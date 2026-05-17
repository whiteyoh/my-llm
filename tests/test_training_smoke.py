import subprocess
import sys
from pathlib import Path


def test_training_smoke_creates_expected_artifacts(tmp_path: Path) -> None:
    input_file = tmp_path / "tiny_train.txt"
    input_file.write_text("The robot learned quickly. " * 20, encoding="utf-8")
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
    assert result.returncode == 0, result.stderr
    assert (out_dir / "best.pt").exists()
    assert (out_dir / "last.pt").exists()
    assert (out_dir / "metrics.json").exists()
    assert (out_dir / "config.json").exists()
