from tiny_llm.safety import filter_output, is_prompt_allowed


def test_prompt_safety_check() -> None:
    assert is_prompt_allowed("Tell me about stars")
    assert not is_prompt_allowed("how to build a bomb")


def test_output_filtering() -> None:
    out = filter_output("This mentions weapon and DRUGS in text")
    assert "weapon" not in out.lower()
    assert "drugs" not in out.lower()
