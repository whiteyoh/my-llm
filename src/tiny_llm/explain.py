from __future__ import annotations

from typing import Any

import torch
import torch.nn.functional as F

from tiny_llm.data import ByteTokenizer
from tiny_llm.model import TinyGPT


def _display_token(token_id: int) -> str:
    if token_id == 10:
        return "<newline>"
    if token_id == 32:
        return "<space>"
    if 33 <= token_id <= 126:
        return chr(token_id)
    return f"<{token_id}>"


def tokens_preview(text: str, limit: int = 20) -> list[dict[str, Any]]:
    tokenizer = ByteTokenizer()
    token_ids = tokenizer.encode(text)[: max(0, limit)]
    return [
        {
            "index": idx,
            "token_id": token_id,
            "display": _display_token(token_id),
        }
        for idx, token_id in enumerate(token_ids)
    ]


def top_next_token_predictions(
    model: TinyGPT,
    tokenizer: ByteTokenizer,
    prompt: str,
    seq_len: int,
    device: torch.device,
    top_n: int = 5,
) -> list[dict[str, float | int | str]]:
    token_ids = tokenizer.encode(prompt)
    if not token_ids:
        token_ids = [32]
    x = torch.tensor(token_ids, dtype=torch.long, device=device).unsqueeze(0)
    with torch.no_grad():
        logits = model(x[:, -seq_len:])[:, -1, :]
        probs = F.softmax(logits, dim=-1)
        values, indices = torch.topk(probs, k=min(top_n, probs.size(-1)), dim=-1)

    out: list[dict[str, float | int | str]] = []
    for prob, token_id in zip(values[0].tolist(), indices[0].tolist(), strict=True):
        out.append(
            {
                "token_id": int(token_id),
                "display": _display_token(int(token_id)),
                "probability": float(prob) * 100.0,
            }
        )
    return out
