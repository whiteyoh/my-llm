import os
from pathlib import Path

import pytest

from tiny_llm.paths import read_sample_text, sample_path


def test_sample_path_resolves_from_project_root() -> None:
    path = sample_path("space_adventure.txt")
    assert path.exists()
    assert path.name == "space_adventure.txt"


def test_read_sample_text_works_from_different_cwd(tmp_path: Path) -> None:
    original = Path.cwd()
    try:
        os.chdir(tmp_path)
        text = read_sample_text("space_adventure.txt")
    finally:
        os.chdir(original)

    assert "Captain Rowan" in text


def test_read_sample_text_falls_back_to_package_data(monkeypatch, tmp_path: Path) -> None:
    import tiny_llm.paths as paths

    monkeypatch.setattr(paths, "SAMPLE_DIR", tmp_path / "missing-samples")

    assert "Captain Rowan" in paths.read_sample_text("space_adventure.txt")
    first = paths.sample_path("space_adventure.txt")
    second = paths.sample_path("space_adventure.txt")
    assert first.exists()
    assert second.exists()
    assert first == second


def test_sample_paths_reject_nested_names() -> None:
    with pytest.raises(ValueError, match="path separators"):
        read_sample_text("../space_adventure.txt")
