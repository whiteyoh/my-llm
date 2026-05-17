import pytest

from tiny_llm.data import ByteTokenizer
from tiny_llm.learn import (
    build_attention_labels,
    build_attention_matrix_rows,
    build_attention_preview,
    build_probability_preview,
    build_token_preview,
    build_training_config,
    create_model_status,
    enforce_teacher_limits,
    generate_learning_output,
    build_restored_learning_state,
    prepare_retrain_comparison,
)
from tiny_llm.model import TinyGPT
from tiny_llm.safety import SafetyConfig


def _tiny_state() -> dict:
    return {
        "model": TinyGPT(256, 16, 32, 4, 1, 0.0),
        "tokenizer": ByteTokenizer(),
        "cfg": {"seq_len": 16},
        "token_count": 20,
        "sequence_count": 4,
        "param_count": 123,
        "train_losses": [2.0, 1.0],
        "val_losses": [2.1, 1.1],
    }


def test_enforce_teacher_limits_classroom_demo() -> None:
    cfg, warnings = enforce_teacher_limits({"seq_len": 128, "d_model": 256, "n_layers": 8, "epochs": 5, "max_new_tokens": 120}, preset="Classroom demo")
    assert cfg["seq_len"] == 32
    assert cfg["d_model"] == 64
    assert cfg["n_layers"] == 2
    assert cfg["epochs"] == 1
    assert cfg["max_new_tokens"] == 40
    assert warnings


def test_enforce_teacher_limits_moderate() -> None:
    cfg, warnings = enforce_teacher_limits({"seq_len": 999, "d_model": 999, "n_layers": 9, "epochs": 8, "max_new_tokens": 140}, preset="Moderate")
    assert cfg["seq_len"] == 64
    assert cfg["d_model"] == 128
    assert cfg["n_layers"] == 4
    assert cfg["epochs"] == 3
    assert cfg["max_new_tokens"] == 80
    assert warnings == ["Teacher controls are keeping this demo CPU-friendly."]


def test_build_training_config_converts_and_limits() -> None:
    cfg, warnings = build_training_config({"seq_len": "128", "d_model": "256", "n_heads": "4", "n_layers": "8", "epochs": "4", "batch_size": "4"}, preset="Classroom demo")
    assert cfg["seq_len"] == 32
    assert isinstance(cfg["seq_len"], int)
    assert warnings


def test_create_model_status_for_none() -> None:
    status = create_model_status(None)
    assert status["trained"] is False


def test_create_model_status_for_state() -> None:
    status = create_model_status(_tiny_state())
    assert status["trained"] is True
    assert status["token_count"] == 20
    assert status["sequence_count"] == 4


def test_prepare_retrain_comparison() -> None:
    assert prepare_retrain_comparison(None, "x") is None
    assert prepare_retrain_comparison("x", None) is None
    assert prepare_retrain_comparison("before", "after") == {"before": "before", "after": "after"}


def test_build_token_preview() -> None:
    preview = build_token_preview("abc", limit=2)
    assert len(preview) == 2
    assert {"index", "token_id", "display"}.issubset(preview[0].keys())


def test_generate_learning_output_safety() -> None:
    state = _tiny_state()
    with pytest.raises(ValueError):
        generate_learning_output(state, "forbidden prompt", max_new_tokens=2, temperature=1.0, top_k=5, safe_cfg=SafetyConfig(enabled=True, banned_terms=("forbidden",)))
    out = generate_learning_output(state, "forbidden prompt", max_new_tokens=2, temperature=1.0, top_k=5, safe_cfg=SafetyConfig(enabled=False, banned_terms=("forbidden",)))
    assert "output" in out


def test_probability_and_attention_preview_work() -> None:
    state = _tiny_state()
    probs = build_probability_preview(state, "hello", top_n=3)
    assert isinstance(probs, list)
    assert len(probs) == 3
    attn = build_attention_preview(state, "hello", limit=8, top_k=2)
    assert "attention_matrix" in attn
    assert "table" in attn


def test_build_attention_labels_prefers_display_and_falls_back_index() -> None:
    tokens = [{"display": "A"}, {}, {"display": "C"}]
    labels = build_attention_labels(tokens)
    assert labels == ["0: A", "1", "2: C"]


def test_build_attention_matrix_rows_include_labels_and_numeric_values() -> None:
    rows = build_attention_matrix_rows([[0.1, 0.9], [0.25, 0.75]], ["0: hi", "1: there"])
    assert rows[0]["token"] == "0: hi"
    assert rows[0]["0: hi"] == pytest.approx(0.1)
    assert isinstance(rows[0]["1: there"], float)
    assert rows[1]["token"] == "1: there"


def test_build_restored_learning_state_contains_expected_fields() -> None:
    model = TinyGPT(256, 16, 32, 4, 1, 0.0)
    metadata = {
        "config": {"seq_len": 32},
        "token_count": 100,
        "sequence_count": 10,
        "train_loss": 1.23,
        "validation_loss": 1.45,
        "param_count": 999,
    }
    defaults = {"seq_len": 16, "d_model": 64, "n_heads": 4, "n_layers": 2, "epochs": 1, "batch_size": 4, "max_new_tokens": 40}
    restored, missing = build_restored_learning_state(model, metadata, defaults)
    assert restored["model"] is model
    assert "tokenizer" in restored
    assert restored["cfg"]["seq_len"] == 32
    assert restored["train_losses"] == [pytest.approx(1.23)]
    assert restored["val_losses"] == [pytest.approx(1.45)]
    assert restored["token_count"] == 100
    assert restored["sequence_count"] == 10
    assert restored["param_count"] == 999
    assert set(missing) == {"d_model", "n_heads", "n_layers", "epochs", "batch_size", "max_new_tokens"}
