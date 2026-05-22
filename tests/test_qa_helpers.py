from tiny_llm.qa import (
    NO_ANSWER_FALLBACK,
    build_qa_prompt,
    extract_answer,
    needs_context_fallback,
    select_context_answer,
)


def test_build_qa_prompt_with_context() -> None:
    prompt = build_qa_prompt("Who is the pilot?", context="Captain Rowan pilots Aurora.")

    assert "Context:" in prompt
    assert "Question: Who is the pilot?" in prompt
    assert "Answer:" in prompt
    assert NO_ANSWER_FALLBACK in prompt


def test_build_qa_prompt_without_context() -> None:
    prompt = build_qa_prompt("Who is the pilot?")

    assert "Context:" not in prompt
    assert "Question: Who is the pilot?" in prompt
    assert prompt.strip().endswith("Answer:")


def test_extract_answer_from_prefixed_output() -> None:
    prompt = build_qa_prompt("Who is the pilot?", context="Captain Rowan pilots Aurora.")
    decoded = prompt + " Captain Rowan is the pilot.\nQuestion: extra turn"

    answer = extract_answer(decoded, prompt)
    assert answer == "Captain Rowan is the pilot."


def test_needs_context_fallback_flags_gibberish() -> None:
    assert needs_context_fallback("t s the t thinthe t")


def test_select_context_answer_returns_best_matching_sentence() -> None:
    context = (
        "Captain Rowan is the pilot of the starship Aurora. "
        "The Aurora departs Mars every month."
    )
    answer = select_context_answer("Who pilots the Aurora?", context)
    assert answer == "Captain Rowan is the pilot of the starship Aurora."


def test_select_context_answer_returns_none_when_no_overlap() -> None:
    context = "The Aurora departs Mars every month."
    answer = select_context_answer("What color is grass?", context)
    assert answer is None
