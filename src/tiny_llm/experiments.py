from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch

from tiny_llm.model import TinyGPT


def make_experiment_metadata(**kwargs: Any) -> dict[str, Any]:
    return {"timestamp": datetime.now(timezone.utc).isoformat(), **kwargs}


def save_experiment(path: str | Path, model: torch.nn.Module, metadata: dict[str, Any]) -> Path:
    base = Path(path)
    base.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), base / "model.pt")
    payload = {**metadata, "checkpoint": "model.pt"}
    (base / "metadata.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return base / "metadata.json"


def load_experiment_metadata(path: str | Path) -> dict[str, Any]:
    meta_path = Path(path) / "metadata.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"Experiment metadata not found: {meta_path}")
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Experiment metadata is corrupted JSON: {meta_path}") from exc


def load_experiment_checkpoint(path: str | Path) -> Path:
    ckpt_path = Path(path) / "model.pt"
    if not ckpt_path.exists():
        raise FileNotFoundError(f"Experiment checkpoint not found: {ckpt_path}")
    return ckpt_path


def experiment_exists(path: str | Path) -> bool:
    base = Path(path)
    return (base / "metadata.json").exists() and (base / "model.pt").exists()


def restore_experiment_model(path: str | Path) -> tuple[TinyGPT, dict[str, Any]]:
    metadata = load_experiment_metadata(path)
    cfg = metadata.get("config") or {}
    model = TinyGPT(256, cfg["seq_len"], cfg["d_model"], cfg["n_heads"], cfg["n_layers"], 0.1)
    state = torch.load(load_experiment_checkpoint(path), map_location="cpu")
    model.load_state_dict(state)
    model.eval()
    return model, metadata


def load_experiment(path: str | Path) -> dict[str, Any]:
    return load_experiment_metadata(path)
