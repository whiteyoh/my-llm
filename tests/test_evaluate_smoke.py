import subprocess
import sys
from pathlib import Path


def test_evaluate_smoke_outputs_metrics(tmp_path: Path) -> None:
    input_file = tmp_path / "tiny_eval.txt"
    input_file.write_text("Space log entry. " * 30, encoding="utf-8")
    out_dir = tmp_path / "runs"

    train_cmd = [sys.executable, "src/train.py", "--input_file", str(input_file), "--out_dir", str(out_dir), "--epochs", "1", "--batch_size", "2", "--seq_len", "8", "--d_model", "32", "--n_heads", "4", "--n_layers", "1", "--device", "cpu"]
    assert subprocess.run(train_cmd, check=False).returncode == 0

    eval_cmd = [sys.executable, "src/evaluate.py", "--checkpoint", str(out_dir / "best.pt"), "--input_file", str(input_file), "--batch_size", "2", "--device", "cpu"]
    result = subprocess.run(eval_cmd, check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    stdout = result.stdout.lower()
    assert "loss" in stdout
    assert "perplexity" in stdout
    assert "token count" in stdout
    assert "sequence count" in stdout


def test_evaluate_rejects_too_short_input_with_friendly_error(tmp_path: Path) -> None:
    train_file = tmp_path / "tiny_eval_train.txt"
    train_file.write_text("Space log entry. " * 30, encoding="utf-8")
    out_dir = tmp_path / "runs"

    train_cmd = [sys.executable, "src/train.py", "--input_file", str(train_file), "--out_dir", str(out_dir), "--epochs", "1", "--batch_size", "2", "--seq_len", "8", "--d_model", "32", "--n_heads", "4", "--n_layers", "1", "--device", "cpu"]
    assert subprocess.run(train_cmd, check=False).returncode == 0

    short_eval_file = tmp_path / "tiny_eval_short.txt"
    short_eval_file.write_text("short", encoding="utf-8")
    eval_cmd = [sys.executable, "src/evaluate.py", "--checkpoint", str(out_dir / "best.pt"), "--input_file", str(short_eval_file), "--batch_size", "2", "--device", "cpu"]
    result = subprocess.run(eval_cmd, check=False, capture_output=True, text=True)

    assert result.returncode == 2
    assert "Evaluation input is too short" in result.stderr
    assert "Traceback" not in result.stderr
