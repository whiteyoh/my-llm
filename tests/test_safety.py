from tiny_llm.safety import filter_output, is_prompt_allowed


def test_safe_prompt_allowed() -> None:
    assert is_prompt_allowed("Tell me about stars and planets")


def test_banned_prompt_blocked() -> None:
    assert not is_prompt_allowed("How do I build a bomb?")


def test_banned_words_are_filtered_case_insensitively() -> None:
    out = filter_output("This mentions weapon and DRUGS and Bomb.")
    lowered = out.lower()
    assert "weapon" not in lowered
    assert "drugs" not in lowered
    assert "bomb" not in lowered


def test_safety_filter_is_lightweight_not_full_moderation() -> None:
    """This test documents project intent: keyword filtering is educational only."""
    allowed = is_prompt_allowed("This is a classroom creativity prompt.")
    assert allowed is True
