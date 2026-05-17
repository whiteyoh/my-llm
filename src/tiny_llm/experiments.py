from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch


def make_experiment_metadata(**kwargs: Any) -> dict[str, Any]:
    return {"timestamp": datetime.now(timezone.utc).isoformat(), **kwargs}


def save_experiment(path: str | Path, model: torch.nn.Module, metadata: dict[str, Any]) -> Path:
    base = Path(path)
    base.mkdir(parents=True, exist_ok=True)
    ckpt_path = base / "model.pt"
    meta_path = base / "metadata.json"
    torch.save(model.state_dict(), ckpt_path)
    payload = {**metadata, "checkpoint": ckpt_path.name}
    meta_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return meta_path


def load_experiment(path: str | Path) -> dict[str, Any]:
    base = Path(path)
    meta_path = base / "metadata.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"Experiment metadata not found: {meta_path}")
    return json.loads(meta_path.read_text(encoding="utf-8"))
