import tiny_llm


def test_package_import() -> None:
    assert tiny_llm.__doc__ is not None
