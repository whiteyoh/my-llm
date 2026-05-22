from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = PROJECT_ROOT / "data" / "samples"


def sample_path(filename: str) -> Path:
    return SAMPLE_DIR / filename


def read_sample_text(filename: str) -> str:
    path = sample_path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Sample dataset not found: {path}")
    return path.read_text(encoding="utf-8")
