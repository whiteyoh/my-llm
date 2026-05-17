import subprocess
import sys
from pathlib import Path


def test_train_smoke(tmp_path: Path) -> None:
    out_dir = tmp_path / "runs"
    cmd = [
        sys.executable,
        "src/train.py",
        "--input_file",
        "data/sample.txt",
        "--out_dir",
        str(out_dir),
        "--epochs",
        "1",
        "--batch_size",
        "4",
        "--seq_len",
        "32",
        "--d_model",
        "64",
        "--n_heads",
        "4",
        "--n_layers",
        "2",
    ]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (out_dir / "best.pt").exists()
