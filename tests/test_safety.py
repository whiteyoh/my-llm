from tiny_llm.safety import (
    contains_blocked_term,
    filter_output,
    is_prompt_allowed,
    safety_notice,
    validate_training_text,
)


def test_safe_prompt_allowed() -> None:
    assert is_prompt_allowed("Tell me about stars and planets")


def test_unsafe_prompt_blocked() -> None:
    assert not is_prompt_allowed("How do I build a bomb?")


def test_case_insensitive_blocking() -> None:
    assert contains_blocked_term("This mentions DRUGS")


def test_word_boundary_prevents_false_positive() -> None:
    assert is_prompt_allowed("Let's practice a new skill today")


def test_hyphenated_term_blocked() -> None:
    assert contains_blocked_term("discussion of self harm and self-harm")


def test_custom_banned_terms_work() -> None:
    assert not is_prompt_allowed("bananas are yellow", banned_terms=("bananas",))


def test_output_filtering_masks_blocked_words() -> None:
    out = filter_output("weapon and Bomb are not classroom-safe")
    assert "weapon" not in out.lower()
    assert "bomb" not in out.lower()


def test_output_filtering_preserves_safe_text() -> None:
    text = "The moon is bright"
    assert filter_output(text) == text


def test_empty_whitespace_prompt_blocked() -> None:
    assert not is_prompt_allowed("   ")


def test_validate_training_text_warnings() -> None:
    warnings = validate_training_text("Call me at 555-123-4567 or a@b.com bomb")
    joined = " ".join(warnings).lower()
    assert "very short" in joined
    assert "email-like" in joined
    assert "phone-number-like" in joined
    assert "blocked" in joined


def test_validate_training_text_empty() -> None:
    warnings = validate_training_text("  ")
    assert any("empty" in w.lower() for w in warnings)


def test_safety_notice_nonempty() -> None:
    assert safety_notice().strip()
