from __future__ import annotations

from typing import Any

import torch

from tiny_llm.data import ByteTokenizer
from tiny_llm.explain import _display_token
from tiny_llm.model import TinyGPT


def format_attention_tokens(token_ids: list[int], limit: int = 24) -> list[dict[str, Any]]:
    shown = token_ids[: max(1, limit)]
    return [{"index": i, "token_id": t, "display": _display_token(t)} for i, t in enumerate(shown)]


def attention_to_table(attn: torch.Tensor, token_ids: list[int], top_k: int = 3) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for i in range(attn.size(0)):
        weights = attn[i]
        k = min(top_k, i + 1)
        vals, idx = torch.topk(weights[: i + 1], k=k)
        rows.append(
            {
                "query_index": i,
                "query_token": _display_token(token_ids[i]),
                "top_attended": [
                    {"index": int(j), "token": _display_token(token_ids[int(j)]), "weight": float(v)}
                    for v, j in zip(vals.tolist(), idx.tolist(), strict=True)
                ],
            }
        )
    return rows


def get_attention_map(
    model: TinyGPT,
    tokenizer: ByteTokenizer,
    prompt: str,
    seq_len: int,
    device: torch.device,
    layer: int = -1,
    head: int = 0,
    limit: int = 24,
) -> dict[str, Any]:
    token_ids = tokenizer.encode(prompt) or [32]
    token_ids = token_ids[-min(seq_len, limit) :]
    x = torch.tensor(token_ids, dtype=torch.long, device=device).unsqueeze(0)
    with torch.no_grad():
        _, attn_maps = model(x, return_attn=True)
    layer_idx = layer if layer >= 0 else len(attn_maps) + layer
    chosen = attn_maps[layer_idx][0, head].detach().cpu()
    return {
        "token_ids": token_ids,
        "tokens": format_attention_tokens(token_ids, limit=limit),
        "attention": chosen,
        "table": attention_to_table(chosen, token_ids),
        "layer": layer_idx,
        "head": head,
    }
