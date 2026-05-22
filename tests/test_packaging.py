from pathlib import Path
import tomllib


def test_console_scripts_are_declared() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    scripts = pyproject["project"]["scripts"]

    assert scripts["kairo-train"] == "tiny_llm.cli:train"
    assert scripts["kairo-generate"] == "tiny_llm.cli:generate"
    assert scripts["kairo-evaluate"] == "tiny_llm.cli:evaluate"
    assert scripts["kairo-chat"] == "tiny_llm.cli:chat"
    assert scripts["kairo-learn"] == "tiny_llm.cli:learn"
