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
from tiny_llm.learn import build_restored_learning_state
from tiny_llm.model import TinyGPT


def _model() -> TinyGPT:
    return TinyGPT(256, 16, 32, 4, 1, 0.0)


def test_save_experiment_writes_metadata_and_model(tmp_path: Path) -> None:
    exp = tmp_path / "exp"
    save_experiment(exp, _model(), make_experiment_metadata(config={"seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 1}))
    assert (exp / "metadata.json").exists()
    assert (exp / "model.pt").exists()


def test_load_experiment_metadata_returns_metadata(tmp_path: Path) -> None:
    exp = tmp_path / "exp"
    save_experiment(exp, _model(), make_experiment_metadata(prompt="hi", config={"seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 1}))
    loaded = load_experiment_metadata(exp)
    assert loaded["prompt"] == "hi"


def test_load_experiment_checkpoint_returns_path(tmp_path: Path) -> None:
    exp = tmp_path / "exp"
    save_experiment(exp, _model(), make_experiment_metadata(config={"seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 1}))
    assert load_experiment_checkpoint(exp) == exp / "model.pt"


def test_experiment_exists_true_false(tmp_path: Path) -> None:
    exp = tmp_path / "exp"
    assert not experiment_exists(exp)
    save_experiment(exp, _model(), make_experiment_metadata(config={"seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 1}))
    assert experiment_exists(exp)


def test_restore_experiment_model_success(tmp_path: Path) -> None:
    exp = tmp_path / "exp"
    save_experiment(exp, _model(), make_experiment_metadata(config={"seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 1}, prompt="hi"))
    restored_model, metadata = restore_experiment_model(exp)
    assert isinstance(restored_model, TinyGPT)
    assert metadata["prompt"] == "hi"


def test_restore_experiment_model_missing_config_raises(tmp_path: Path) -> None:
    exp = tmp_path / "exp"
    save_experiment(exp, _model(), make_experiment_metadata(prompt="hi"))
    with pytest.raises(ValueError, match="missing model config"):
        restore_experiment_model(exp)


def test_corrupted_metadata_json_raises_friendly_value_error(tmp_path: Path) -> None:
    exp = tmp_path / "exp"
    exp.mkdir()
    (exp / "metadata.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="corrupted JSON"):
        load_experiment_metadata(exp)


def test_missing_metadata_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_experiment_metadata(tmp_path / "missing")


def test_build_restored_learning_state_uses_safe_defaults() -> None:
    model = _model()
    state, missing = build_restored_learning_state(model, {"prompt": "hi"}, defaults={"seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 1})
    assert set(missing) == {"seq_len", "d_model", "n_heads", "n_layers"}
    assert state["cfg"]["seq_len"] == 16
    assert state["train_losses"] == [0.0]
