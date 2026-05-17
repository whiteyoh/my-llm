from pathlib import Path


from tiny_llm.experiments import load_experiment, make_experiment_metadata, save_experiment
from tiny_llm.model import TinyGPT


def test_metadata_creation() -> None:
    meta = make_experiment_metadata(token_count=42)
    assert "timestamp" in meta
    assert meta["token_count"] == 42


def test_save_load_roundtrip(tmp_path: Path) -> None:
    model = TinyGPT(256, 16, 32, 4, 1, 0.0)
    meta = make_experiment_metadata(prompt="hi")
    save_experiment(tmp_path / "exp1", model, meta)
    loaded = load_experiment(tmp_path / "exp1")
    assert loaded["prompt"] == "hi"
    assert (tmp_path / "exp1" / "model.pt").exists()


def test_missing_file_handling(tmp_path: Path) -> None:
    try:
        load_experiment(tmp_path / "missing")
        assert False
    except FileNotFoundError:
        assert True
