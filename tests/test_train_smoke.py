import subprocess
import sys
from pathlib import Path


def test_train_generate_evaluate_smoke(tmp_path: Path) -> None:
    out_dir = tmp_path / "runs"
    train_cmd = [
        sys.executable,
        "src/train.py",
        "--input_file",
        "data/samples/space_adventure.txt",
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
    assert subprocess.run(train_cmd, check=False).returncode == 0
    assert (out_dir / "best.pt").exists()

    gen_cmd = [
        sys.executable,
        "src/generate.py",
        "--checkpoint",
        str(out_dir / "best.pt"),
        "--prompt",
        "hello",
        "--max_new_tokens",
        "4",
    ]
    assert subprocess.run(gen_cmd, check=False).returncode == 0

    eval_cmd = [
        sys.executable,
        "src/evaluate.py",
        "--checkpoint",
        str(out_dir / "best.pt"),
        "--input_file",
        "data/samples/space_adventure.txt",
        "--batch_size",
        "4",
    ]
    assert subprocess.run(eval_cmd, check=False).returncode == 0
