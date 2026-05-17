from __future__ import annotations

import random

import numpy as np
import torch
import torch.nn.functional as F

from tiny_llm.data import ByteTokenizer
from tiny_llm.model import TinyGPT


def resolve_device(device: str) -> torch.device:
    if device not in {"auto", "cpu", "cuda"}:
        raise ValueError("device must be one of: auto, cpu, cuda")
    if device == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cuda requested but not available")
    return torch.device(device)


def validate_sampling_args(max_new_tokens: int, temperature: float, top_k: int, top_p: float) -> None:
    if max_new_tokens <= 0:
        raise ValueError("max_new_tokens must be > 0")
    if temperature <= 0:
        raise ValueError("temperature must be > 0")
    if top_k < 0:
        raise ValueError("top_k must be >= 0")
    if not (0.0 < top_p <= 1.0):
        raise ValueError("top_p must be in (0, 1]")


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)


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
