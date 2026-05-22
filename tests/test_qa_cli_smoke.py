import subprocess
import sys
from pathlib import Path


def test_build_qa_corpus_cli_smoke(tmp_path: Path) -> None:
    jsonl = tmp_path / "qa.jsonl"
    jsonl.write_text(
        "\n".join(
            [
                '{"context":"Mars is red.","question":"What color is Mars?","answer":"Mars is red."}',
                '{"question":"Who pilots Aurora?","answer":"Captain Rowan."}',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    out_file = tmp_path / "qa_train.txt"

    cmd = [sys.executable, "src/build_qa_corpus.py", "--input_jsonl", str(jsonl), "--output_file", str(out_file)]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    assert out_file.exists()
    text = out_file.read_text(encoding="utf-8")
    assert "Question: What color is Mars?" in text
    assert "Answer: Mars is red." in text


def test_build_qa_corpus_accepts_bundled_sample_name(tmp_path: Path) -> None:
    out_file = tmp_path / "qa_from_bundle.txt"
    cmd = [
        sys.executable,
        "src/build_qa_corpus.py",
        "--input_jsonl",
        "qa_space_facts.jsonl",
        "--output_file",
        str(out_file),
    ]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    assert out_file.exists()
    out_text = out_file.read_text(encoding="utf-8")
    assert "Question: Who pilots the starship Aurora?" in out_text


def test_qa_cli_missing_context_file_is_friendly() -> None:
    cmd = [
        sys.executable,
        "src/qa.py",
        "--checkpoint",
        "runs/missing/best.pt",
        "--question",
        "Who pilots Aurora?",
        "--context_file",
        "runs/missing/context.txt",
    ]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)

    assert result.returncode == 2
    assert "Context file not found" in result.stderr
    assert "Traceback" not in result.stderr


def test_qa_cli_smoke_with_context(tmp_path: Path) -> None:
    train_text = tmp_path / "qa_train.txt"
    train_text.write_text(
        "\n".join(
            [
                "Context:",
                "Captain Rowan is the pilot of the starship Aurora.",
                "",
                "Question: Who pilots the Aurora?",
                "Answer: Captain Rowan pilots the Aurora.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    out_dir = tmp_path / "runs"

    train_cmd = [
        sys.executable,
        "src/train.py",
        "--input_file",
        str(train_text),
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
    assert subprocess.run(train_cmd, check=False).returncode == 0

    qa_cmd = [
        sys.executable,
        "src/qa.py",
        "--checkpoint",
        str(out_dir / "best.pt"),
        "--question",
        "Who pilots the Aurora?",
        "--context",
        "Captain Rowan is the pilot of the starship Aurora.",
        "--seed",
        "42",
        "--max_new_tokens",
        "16",
        "--device",
        "cpu",
    ]
    result = subprocess.run(qa_cmd, check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    assert "Kairo QA" in result.stdout
    assert "Answer:" in result.stdout
    assert "Traceback" not in result.stderr
