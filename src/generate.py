from __future__ import annotations

import argparse
import random

import numpy as np
import torch
import torch.nn.functional as F

from tiny_llm.data import ByteTokenizer
from tiny_llm.model import TinyGPT
from tiny_llm.utils import load_checkpoint


def resolve_device(device: str) -> torch.device:
    if device == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(device)


def sample_next_token(logits: torch.Tensor, temperature: float, top_k: int, top_p: float) -> int:
    logits = logits / temperature

    if top_k > 0:
        values, _ = torch.topk(logits, k=min(top_k, logits.size(-1)))
        cutoff = values[..., -1, None]
        logits = torch.where(logits < cutoff, torch.full_like(logits, float("-inf")), logits)

    if top_p < 1.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True, dim=-1)
        sorted_probs = F.softmax(sorted_logits, dim=-1)
        cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
        sorted_mask = cumulative_probs > top_p
        sorted_mask[..., 1:] = sorted_mask[..., :-1].clone()
        sorted_mask[..., 0] = False
        filtered_sorted_logits = sorted_logits.masked_fill(sorted_mask, float("-inf"))
        logits = torch.full_like(logits, float("-inf"))
        logits.scatter_(dim=-1, index=sorted_indices, src=filtered_sorted_logits)

    probs = F.softmax(logits, dim=-1)
    next_token = torch.multinomial(probs, num_samples=1)
    token_id = int(next_token.item())
    return max(0, min(token_id, logits.size(-1) - 1))


def generate_tokens(
    model: TinyGPT,
    prompt: str,
    tokenizer: ByteTokenizer,
    seq_len: int,
    max_new_tokens: int,
    temperature: float,
    top_k: int,
    top_p: float,
    device: torch.device,
) -> list[int]:
    tokens = tokenizer.encode(prompt)
    x = torch.tensor(tokens, dtype=torch.long, device=device).unsqueeze(0)
    for _ in range(max_new_tokens):
        x_cond = x[:, -seq_len:]
        logits = model(x_cond)
        next_token = sample_next_token(logits[:, -1, :], temperature, top_k, top_p)
        x = torch.cat([x, torch.tensor([[next_token]], dtype=torch.long, device=device)], dim=1)
    return x[0].tolist()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate text from a trained tiny GPT model.")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--max_new_tokens", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--top_k", type=int, default=40)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "cpu", "cuda"])
    args = parser.parse_args()

    if args.max_new_tokens <= 0:
        raise ValueError("max_new_tokens must be > 0")
    if args.temperature <= 0:
        raise ValueError("temperature must be > 0")
    if args.top_k < 0:
        raise ValueError("top_k must be >= 0")
    if not (0.0 < args.top_p <= 1.0):
        raise ValueError("top_p must be in (0, 1]")

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)
        torch.manual_seed(args.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(args.seed)

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
    with torch.no_grad():
        out_ids = generate_tokens(
            model,
            args.prompt,
            tokenizer,
            seq_len=config["seq_len"],
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            top_k=args.top_k,
            top_p=args.top_p,
            device=device,
        )
    print(tokenizer.decode(out_ids))


if __name__ == "__main__":
    main()
