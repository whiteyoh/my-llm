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


def test_package_data_includes_sample_texts() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert "py-modules" not in pyproject["tool"]["setuptools"]
    assert pyproject["tool"]["setuptools"]["package-data"]["tiny_llm"] == ["samples/*.txt"]


def test_source_samples_are_copied_into_package() -> None:
    source_samples = sorted(path.name for path in Path("data/samples").glob("*.txt"))
    package_samples = sorted(path.name for path in Path("src/tiny_llm/samples").glob("*.txt"))

    assert source_samples
    assert package_samples == source_samples


def test_console_wrappers_import_package_modules(monkeypatch) -> None:
    from tiny_llm import cli

    module_names = []
    monkeypatch.setattr(cli, "_run_main", module_names.append)

    cli.train()
    cli.generate()
    cli.evaluate()
    cli.chat()

    assert module_names == [
        "tiny_llm.train",
        "tiny_llm.generate",
        "tiny_llm.evaluate",
        "tiny_llm.chat",
    ]
