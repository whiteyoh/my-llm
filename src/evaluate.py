from __future__ import annotations

import argparse
import math
from pathlib import Path

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

from tiny_llm.data import ByteTokenizer, SequenceDataset
from tiny_llm.generation import resolve_device
from tiny_llm.model import TinyGPT
from tiny_llm.utils import load_checkpoint


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate checkpoint perplexity on a text file.")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "cpu", "cuda"])
    args = parser.parse_args()

    if args.batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    device = resolve_device(args.device)
    ckpt = load_checkpoint(args.checkpoint, map_location=device)
    config = ckpt["config"]

    model = TinyGPT(
        vocab_size=config["vocab_size"],
        seq_len=config["seq_len"],
        d_model=config["d_model"],
        n_heads=config["n_heads"],
        n_layers=config["n_layers"],
        dropout=config["dropout"],
    ).to(device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()

    tokenizer = ByteTokenizer()
    text = Path(args.input_file).read_text(encoding="utf-8")
    token_ids = tokenizer.encode(text)
    dataset = SequenceDataset(token_ids, seq_len=config["seq_len"])
    loader = DataLoader(dataset, batch_size=args.batch_size)

    total_loss = 0.0
    batches = 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
            total_loss += loss.item()
            batches += 1

    avg_loss = total_loss / max(1, batches)
    perplexity = math.exp(avg_loss)
    print("=== Kairo Evaluation ===")
    print(f"loss: {avg_loss:.6f}")
    print(f"perplexity: {perplexity:.6f}")
    print(f"token count: {len(token_ids)}")
    print(f"sequence count: {len(dataset)}")
    print("Perplexity is the model's uncertainty: lower is generally better for this dataset.")


if __name__ == "__main__":
    main()
