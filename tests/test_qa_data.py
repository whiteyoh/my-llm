from pathlib import Path

import pytest

from tiny_llm.qa_data import build_corpus_text, load_jsonl, resolve_input_jsonl


def test_build_corpus_text_formats_records() -> None:
    records = [
        {"context": "Mars is red.", "question": "What color is Mars?", "answer": "Mars is red."},
        {"q": "Who pilots Aurora?", "a": "Captain Rowan."},
    ]

    text = build_corpus_text(records)

    assert "Context:" in text
    assert "Question: What color is Mars?" in text
    assert "Answer: Mars is red." in text
    assert "Question: Who pilots Aurora?" in text
    assert "Answer: Captain Rowan." in text


def test_build_corpus_text_rejects_missing_answer() -> None:
    with pytest.raises(ValueError, match="missing a non-empty answer field"):
        build_corpus_text([{"question": "Who pilots Aurora?"}])


def test_load_jsonl_skips_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "qa.jsonl"
    path.write_text('\n{"question":"Q1","answer":"A1"}\n\n{"question":"Q2","answer":"A2"}\n', encoding="utf-8")

    records = load_jsonl(path)
    assert len(records) == 2


def test_resolve_input_jsonl_uses_bundled_sample_name() -> None:
    resolved = resolve_input_jsonl("qa_space_facts.jsonl")
    assert resolved.exists()
    assert resolved.name == "qa_space_facts.jsonl"
