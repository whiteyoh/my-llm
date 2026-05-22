import os
from pathlib import Path

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
