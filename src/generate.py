from __future__ import annotations

import argparse

import torch
import torch.nn.functional as F

from tiny_llm.data import ByteTokenizer
from tiny_llm.model import TinyGPT


def sample_next_token(logits: torch.Tensor, temperature: float, top_k: int, top_p: float) -> int:
    logits = logits / max(temperature, 1e-6)

    if top_k > 0:
        values, _ = torch.topk(logits, k=min(top_k, logits.size(-1)))
        cutoff = values[..., -1, None]
        logits = torch.where(logits < cutoff, torch.full_like(logits, float("-inf")), logits)

    if 0.0 < top_p < 1.0:
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
    return int(torch.multinomial(probs, num_samples=1).item())


def safe_load_checkpoint(path: str) -> dict:
    try:
        # PyTorch 2.1+ supports weights_only to reduce unsafe pickle loading.
        return torch.load(path, map_location="cpu", weights_only=True)
    except TypeError:
        # Fallback for older torch versions that do not support weights_only.
        return torch.load(path, map_location="cpu")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate text from a trained tiny GPT model.")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--max_new_tokens", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--top_k", type=int, default=40)
    parser.add_argument("--top_p", type=float, default=1.0)
    args = parser.parse_args()

    ckpt = safe_load_checkpoint(args.checkpoint)
    config = ckpt["config"]

    model = TinyGPT(
        vocab_size=config["vocab_size"],
        seq_len=config["seq_len"],
        d_model=config["d_model"],
        n_heads=config["n_heads"],
        n_layers=config["n_layers"],
        dropout=config["dropout"],
    )
    model.load_state_dict(ckpt["model_state"])
    model.eval()

    tokenizer = ByteTokenizer()
    tokens = tokenizer.encode(args.prompt)
    x = torch.tensor(tokens, dtype=torch.long).unsqueeze(0)

    for _ in range(args.max_new_tokens):
        x_cond = x[:, -config["seq_len"] :]
        logits = model(x_cond)
        next_token = sample_next_token(logits[:, -1, :], args.temperature, args.top_k, args.top_p)
        x = torch.cat([x, torch.tensor([[next_token]], dtype=torch.long)], dim=1)

    print(tokenizer.decode(x[0].tolist()))


if __name__ == "__main__":
    main()
