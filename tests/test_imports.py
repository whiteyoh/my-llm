import importlib.util

import pytest


def test_package_import() -> None:
    import tiny_llm

    assert tiny_llm.__doc__ is not None
    __import__("tiny_llm.agents_runtime")
    __import__("tiny_llm.qa")
    __import__("tiny_llm.qa_data")


def test_kairo_learn_import_only_when_streamlit_is_available() -> None:
    """Learn Mode is optional in tests because streamlit is not a default dependency."""
    if importlib.util.find_spec("streamlit") is None:
        pytest.skip("streamlit not installed; skipping Learn Mode import smoke test")

    __import__("tiny_llm.kairo_learn")
    __import__("tiny_llm.agents_dashboard")
