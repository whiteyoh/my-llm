from __future__ import annotations

import json
from pathlib import Path

import torch


def save_json(path: str | Path, payload: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def load_checkpoint(path: str | Path, map_location: str | torch.device = "cpu") -> dict:
    try:
        return torch.load(path, map_location=map_location, weights_only=True)
    except TypeError:
        # Older PyTorch versions may not support weights_only; only use this fallback for trusted local files.
        return torch.load(path, map_location=map_location)
