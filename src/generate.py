from __future__ import annotations

import argparse

import torch
import torch.nn.functional as F

from tiny_llm.data import ByteTokenizer
from tiny_llm.model import TinyGPT


def sample_next_token(logits: torch.Tensor, temperature: float, top_k: int) -> int:
    logits = logits / max(temperature, 1e-6)
    if top_k > 0:
        values, _ = torch.topk(logits, k=min(top_k, logits.size(-1)))
        cutoff = values[..., -1, None]
        logits = torch.where(logits < cutoff, torch.full_like(logits, float("-inf")), logits)
    probs = F.softmax(logits, dim=-1)
    return int(torch.multinomial(probs, num_samples=1).item())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate text from a trained tiny GPT model.")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--max_new_tokens", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--top_k", type=int, default=40)
    args = parser.parse_args()

    ckpt = torch.load(args.checkpoint, map_location="cpu")
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
        next_token = sample_next_token(logits[:, -1, :], args.temperature, args.top_k)
        x = torch.cat([x, torch.tensor([[next_token]], dtype=torch.long)], dim=1)

    print(tokenizer.decode(x[0].tolist()))


if __name__ == "__main__":
    main()
