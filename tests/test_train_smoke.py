import subprocess
import sys
from pathlib import Path


def test_train_generate_evaluate_smoke(tmp_path: Path) -> None:
    out_dir = tmp_path / "runs"
    train_cmd = [
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
    train_res = subprocess.run(train_cmd, check=False, capture_output=True, text=True)
    assert train_res.returncode == 0, train_res.stderr
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
    gen_res = subprocess.run(gen_cmd, check=False, capture_output=True, text=True)
    assert gen_res.returncode == 0, gen_res.stderr

    eval_cmd = [
        sys.executable,
        "src/evaluate.py",
        "--checkpoint",
        str(out_dir / "best.pt"),
        "--input_file",
        "data/sample.txt",
        "--batch_size",
        "4",
    ]
    eval_res = subprocess.run(eval_cmd, check=False, capture_output=True, text=True)
    assert eval_res.returncode == 0, eval_res.stderr
    assert "perplexity:" in eval_res.stdout
