import subprocess
import sys
from pathlib import Path


def test_generate_cli_smoke(tmp_path: Path) -> None:
    input_file = tmp_path / "tiny_cli.txt"
    input_file.write_text("The robot opened the hatch. " * 20, encoding="utf-8")
    out_dir = tmp_path / "runs"

    train_cmd = [sys.executable, "src/train.py", "--input_file", str(input_file), "--out_dir", str(out_dir), "--epochs", "1", "--batch_size", "2", "--seq_len", "8", "--d_model", "32", "--n_heads", "4", "--n_layers", "1", "--device", "cpu"]
    assert subprocess.run(train_cmd, check=False).returncode == 0

    gen_cmd = [sys.executable, "src/generate.py", "--checkpoint", str(out_dir / "best.pt"), "--prompt", "The robot", "--max_new_tokens", "5", "--device", "cpu"]
    result = subprocess.run(gen_cmd, check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    assert "Kairo Generation" in result.stdout
    assert "Generated output" in result.stdout


def test_generate_cli_missing_checkpoint_is_friendly() -> None:
    cmd = [
        sys.executable,
        "src/generate.py",
        "--checkpoint",
        "runs/missing/best.pt",
        "--prompt",
        "The robot",
        "--max_new_tokens",
        "5",
        "--device",
        "cpu",
    ]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)

    assert result.returncode == 2
    assert "Checkpoint not found" in result.stderr
    assert "Traceback" not in result.stderr


def test_generate_cli_rejects_empty_prompt() -> None:
    cmd = [
        sys.executable,
        "src/generate.py",
        "--checkpoint",
        "runs/missing/best.pt",
        "--prompt",
        "   ",
        "--max_new_tokens",
        "5",
        "--device",
        "cpu",
    ]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)

    assert result.returncode == 2
    assert "prompt must not be empty" in result.stderr
    assert "Traceback" not in result.stderr


def test_train_cli_rejects_too_short_training_text(tmp_path: Path) -> None:
    input_file = tmp_path / "too_short.txt"
    input_file.write_text("123456789", encoding="utf-8")
    out_dir = tmp_path / "runs"

    cmd = [
        sys.executable,
        "src/train.py",
        "--input_file",
        str(input_file),
        "--out_dir",
        str(out_dir),
        "--epochs",
        "1",
        "--batch_size",
        "2",
        "--seq_len",
        "8",
        "--d_model",
        "32",
        "--n_heads",
        "4",
        "--n_layers",
        "1",
        "--device",
        "cpu",
    ]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)

    assert result.returncode == 2
    assert "Training text is too short" in result.stderr
    assert "Traceback" not in result.stderr
    assert not out_dir.exists()
