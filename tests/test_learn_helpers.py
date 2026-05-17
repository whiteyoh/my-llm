import pytest

from tiny_llm.learn import build_attention_labels, build_attention_matrix_rows, build_training_config, enforce_teacher_limits, generate_learning_output, prepare_retrain_comparison
from tiny_llm.model import TinyGPT
from tiny_llm.safety import SafetyConfig


def _state():
    from tiny_llm.data import ByteTokenizer

    tok = ByteTokenizer()
    model = TinyGPT(256, 16, 32, 4, 1, 0.0)
    return {"model": model, "tokenizer": tok, "cfg": {"seq_len": 16}}


def test_teacher_limits_enforced() -> None:
    cfg, warnings = build_training_config({"seq_len": 128, "d_model": 256, "n_heads": 4, "n_layers": 8, "epochs": 8, "batch_size": 4}, preset="Classroom demo")
    assert cfg["seq_len"] == 32
    assert cfg["d_model"] == 64
    assert cfg["n_layers"] == 2
    assert cfg["epochs"] == 1
    assert warnings == ["Teacher controls are keeping this demo CPU-friendly."]


def test_max_new_tokens_clamped() -> None:
    cfg, warnings = enforce_teacher_limits({"max_new_tokens": 500}, preset="Moderate")
    assert cfg["max_new_tokens"] == 80
    assert warnings


def test_retrain_comparison_helper() -> None:
    assert prepare_retrain_comparison("a", "b") == {"before": "a", "after": "b"}


def test_custom_banned_terms_enforced() -> None:
    state = _state()
    with pytest.raises(ValueError):
        generate_learning_output(state, "forbidden", max_new_tokens=2, temperature=1.0, top_k=5, safe_cfg=SafetyConfig(enabled=True, banned_terms=("forbidden",)))


def test_attention_labels_use_display_when_present() -> None:
    labels = build_attention_labels([{"display": "h"}, {"display": "<space>"}, {}])
    assert labels == ["0: h", "1: <space>", "2"]


def test_attention_matrix_rows_add_named_columns() -> None:
    rows = build_attention_matrix_rows([[1.0, 0.0], [0.2, 0.8]], ["0: h", "1: i"])
    assert rows[0]["token"] == "0: h"
    assert rows[1]["1: i"] == pytest.approx(0.8)
