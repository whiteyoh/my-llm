from pathlib import Path

import pytest

from tiny_llm.experiments import (
    experiment_exists,
    load_experiment_checkpoint,
    load_experiment_metadata,
    make_experiment_metadata,
    restore_experiment_model,
    save_experiment,
)
from tiny_llm.model import TinyGPT


def test_metadata_creation() -> None:
    meta = make_experiment_metadata(token_count=42)
    assert "timestamp" in meta


def test_save_load_roundtrip_and_restore(tmp_path: Path) -> None:
    model = TinyGPT(256, 16, 32, 4, 1, 0.0)
    meta = make_experiment_metadata(config={"seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 1}, prompt="hi")
    save_experiment(tmp_path / "exp1", model, meta)
    loaded = load_experiment_metadata(tmp_path / "exp1")
    assert loaded["prompt"] == "hi"
    assert experiment_exists(tmp_path / "exp1")
    assert load_experiment_checkpoint(tmp_path / "exp1").exists()
    restored_model, restored_meta = restore_experiment_model(tmp_path / "exp1")
    assert isinstance(restored_model, TinyGPT)
    assert restored_meta["prompt"] == "hi"


def test_missing_and_corrupt_metadata(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_experiment_metadata(tmp_path / "missing")
    exp = tmp_path / "exp2"
    exp.mkdir()
    (exp / "metadata.json").write_text("{bad", encoding="utf-8")
    with pytest.raises(ValueError):
        load_experiment_metadata(exp)
