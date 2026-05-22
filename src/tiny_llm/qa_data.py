from __future__ import annotations

import argparse
import json
from pathlib import Path

from tiny_llm.paths import sample_path


def _first_present(record: dict, keys: tuple[str, ...]) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def format_qa_example(question: str, answer: str, context: str = "") -> str:
    lines: list[str] = []
    if context.strip():
        lines.extend(["Context:", context.strip(), ""])
    lines.extend(
        [
            f"Question: {question.strip()}",
            f"Answer: {answer.strip()}",
            "",
        ]
    )
    return "\n".join(lines)


def build_corpus_text(records: list[dict]) -> str:
    blocks: list[str] = []
    for i, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Record {i} is not a JSON object")

        question = _first_present(record, ("question", "q", "prompt"))
        answer = _first_present(record, ("answer", "a", "response"))
        context = _first_present(record, ("context", "passage"))
        if not question:
            raise ValueError(f"Record {i} is missing a non-empty question field")
        if not answer:
            raise ValueError(f"Record {i} is missing a non-empty answer field")
        blocks.append(format_qa_example(question, answer, context=context))
    return "\n".join(blocks)


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on line {line_number}: {exc.msg}") from exc
        records.append(obj)
    return records


def resolve_input_jsonl(user_value: str) -> Path:
    explicit_path = Path(user_value)
    if explicit_path.exists():
        return explicit_path

    sample_name = explicit_path.name
    if sample_name:
        try:
            return sample_path(sample_name)
        except (FileNotFoundError, ValueError):
            pass

    raise FileNotFoundError(
        f"QA dataset file not found: {explicit_path}. "
        "Provide a valid path or a bundled sample name like qa_space_facts.jsonl."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert JSONL question/answer records into Kairo training text.")
    parser.add_argument("--input_jsonl", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    args = parser.parse_args()

    try:
        input_path = resolve_input_jsonl(args.input_jsonl)
    except FileNotFoundError as exc:
        parser.exit(2, f"{exc}\n")

    try:
        records = load_jsonl(input_path)
        corpus = build_corpus_text(records)
    except ValueError as exc:
        parser.exit(2, f"{exc}\n")

    if not corpus.strip():
        parser.exit(2, "QA dataset produced no training text after parsing.\n")

    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(corpus, encoding="utf-8")
    print(f"Wrote {len(records)} QA records to {output_path}")


if __name__ == "__main__":
    main()
