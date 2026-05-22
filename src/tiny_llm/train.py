from __future__ import annotations

import argparse
from pathlib import Path

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split

from tiny_llm.data import ByteTokenizer, SequenceDataset
from tiny_llm.generation import resolve_device, set_seed
from tiny_llm.model import TinyGPT
from tiny_llm.safety import validate_training_text
from tiny_llm.training import train_val_split_sizes, validate_training_token_count
from tiny_llm.utils import load_checkpoint, save_json


def evaluate(model: TinyGPT, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    losses = []
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
            losses.append(loss.item())
    return float(sum(losses) / max(1, len(losses)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a tiny GPT-style language model.")
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--out_dir", type=str, default="runs/default")
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--seq_len", type=int, default=128)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--d_model", type=int, default=256)
    parser.add_argument("--n_heads", type=int, default=8)
    parser.add_argument("--n_layers", type=int, default=6)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--val_ratio", type=float, default=0.1)
    parser.add_argument("--grad_clip", type=float, default=1.0)
    parser.add_argument("--resume", type=str, default="")
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--amp", action="store_true", help="Enable mixed precision when running on CUDA")
    args = parser.parse_args()

    if args.batch_size <= 0:
        parser.error("batch_size must be > 0")
    if args.seq_len <= 0:
        parser.error("seq_len must be > 0")
    if args.epochs <= 0:
        parser.error("epochs must be > 0")
    if args.lr <= 0:
        parser.error("lr must be > 0")
    if not (0.0 < args.val_ratio < 1.0):
        parser.error("val_ratio must be in (0, 1)")

    set_seed(args.seed)
    out_dir = Path(args.out_dir)

    input_path = Path(args.input_file)
    if not input_path.exists():
        parser.exit(2, f"Training input file not found: {input_path}\n")

    text = input_path.read_text(encoding="utf-8")
    for warning in validate_training_text(text):
        print(f"[safety warning] {warning}")
    tokenizer = ByteTokenizer()
    token_ids = tokenizer.encode(text)
    try:
        validate_training_token_count(len(token_ids), args.seq_len)
    except ValueError as exc:
        parser.exit(2, f"{exc}\n")
    dataset = SequenceDataset(token_ids, seq_len=args.seq_len)

    try:
        train_size, val_size = train_val_split_sizes(len(dataset), args.val_ratio)
    except ValueError as exc:
        parser.exit(2, f"{exc}\n")
    split_generator = torch.Generator().manual_seed(args.seed)
    train_ds, val_ds = random_split(dataset, [train_size, val_size], generator=split_generator)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size)

    device = resolve_device(args.device)
    model = TinyGPT(
        vocab_size=tokenizer.vocab_size,
        seq_len=args.seq_len,
        d_model=args.d_model,
        n_heads=args.n_heads,
        n_layers=args.n_layers,
        dropout=args.dropout,
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
    use_amp = bool(args.amp and device.type == "cuda")
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    history: dict[str, list[float]] = {"train_loss": [], "val_loss": []}
    best_val = float("inf")
    start_epoch = 1
    config = vars(args) | {"vocab_size": tokenizer.vocab_size, "device": str(device)}

    if args.resume:
        try:
            ckpt = load_checkpoint(Path(args.resume), map_location=device)
        except FileNotFoundError as exc:
            parser.exit(2, f"{exc}\n")
        model.load_state_dict(ckpt["model_state"])
        if "optimizer_state" in ckpt:
            optimizer.load_state_dict(ckpt["optimizer_state"])
        start_epoch = int(ckpt.get("epoch", 0)) + 1
        best_val = float(ckpt.get("best_val", best_val))
        history = ckpt.get("history", history)
        config = ckpt.get("config", config)

    out_dir.mkdir(parents=True, exist_ok=True)
    save_json(out_dir / "config.json", config)
    total_params = sum(p.numel() for p in model.parameters())
    print("=== Kairo training ===")
    print(f"Device: {device}")
    print(f"Parameters: {total_params:,}")
    print(f"Dataset token count: {len(dataset):,} sequences from {len(text):,} bytes of text")
    print(f"Train/validation split: {train_size:,} / {val_size:,} sequences")
    print(f"Checkpoint output paths: best={out_dir / 'best.pt'} last={out_dir / 'last.pt'}")
    print(f"AMP mixed precision: {'enabled' if use_amp else 'disabled'}")

    for epoch in range(start_epoch, args.epochs + 1):
        model.train()
        running = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda", enabled=use_amp):
                logits = model(x)
                loss = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
            scaler.scale(loss).backward()
            if args.grad_clip > 0:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip)
            scaler.step(optimizer)
            scaler.update()
            running += loss.item()

        train_loss = running / max(1, len(train_loader))
        val_loss = evaluate(model, val_loader, device)
        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        print(f"Epoch {epoch}/{args.epochs} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f}")

        ckpt = {
            "model_state": model.state_dict(),
            "optimizer_state": optimizer.state_dict(),
            "config": config,
            "epoch": epoch,
            "best_val": best_val,
            "history": history,
        }
        torch.save(ckpt, out_dir / "last.pt")
        if val_loss < best_val:
            best_val = val_loss
            ckpt["best_val"] = best_val
            torch.save(ckpt, out_dir / "best.pt")
            print(f"Saved new best checkpoint: {out_dir / 'best.pt'}")

    save_json(out_dir / "metrics.json", history)
    print(f"Training complete. Last checkpoint: {out_dir / 'last.pt'}")


if __name__ == "__main__":
    main()
