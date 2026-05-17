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
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0 so learners can inspect attended tokens.")
    rows: list[dict[str, Any]] = []
    for i in range(attn.size(0)):
        weights = attn[i]
        k = min(top_k, i + 1)
        vals, idx = torch.topk(weights[: i + 1], k=k)
        rows.append({"query_index": i, "query_token": _display_token(token_ids[i]), "top_attended": [{"index": int(j), "token": _display_token(token_ids[int(j)]), "weight": float(v)} for v, j in zip(vals.tolist(), idx.tolist(), strict=True)]})
    return rows


def get_attention_map(model: TinyGPT, tokenizer: ByteTokenizer, prompt: str, seq_len: int, device: torch.device, layer: int = -1, head: int = 0, limit: int = 24, top_k: int = 3) -> dict[str, Any]:
    if not prompt.strip():
        raise ValueError("Prompt is empty. Add a few words to inspect attention.")
    if limit <= 0:
        raise ValueError("limit must be greater than 0 so attention rows can be shown.")
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0 so learners can inspect attended tokens.")
    token_ids = tokenizer.encode(prompt)
    token_ids = token_ids[-min(seq_len, limit) :]
    x = torch.tensor(token_ids, dtype=torch.long, device=device).unsqueeze(0)
    with torch.no_grad():
        _, attn_maps = model(x, return_attn=True)
    layer_idx = layer if layer >= 0 else len(attn_maps) + layer
    if layer_idx < 0 or layer_idx >= len(attn_maps):
        raise ValueError(f"Invalid layer index {layer}. Choose between -{len(attn_maps)} and {len(attn_maps)-1}.")
    if head < 0 or head >= attn_maps[layer_idx].size(1):
        raise ValueError(f"Invalid head index {head}. Choose between 0 and {attn_maps[layer_idx].size(1)-1}.")
    chosen = attn_maps[layer_idx][0, head].detach().cpu()
    return {
        "token_ids": token_ids,
        "token_labels": format_attention_tokens(token_ids, limit=limit),
        "tokens": format_attention_tokens(token_ids, limit=limit),
        "attention": chosen,
        "attention_tensor": chosen,
        "attention_matrix": chosen.tolist(),
        "table": attention_to_table(chosen, token_ids, top_k=top_k),
        "selected_layer": layer_idx,
        "selected_head": head,
        "token_count": len(token_ids),
        "layer": layer_idx,
        "head": head,
        "num_tokens": len(token_ids),
        "note": "Attention is a model mechanism, not human understanding.",
    }
