from __future__ import annotations

from pathlib import Path
import re


BOOK_MD = Path("docs/tech_i_can_kairo_book.md")


def _lines() -> list[str]:
    return BOOK_MD.read_text(encoding="utf-8").splitlines()


def test_book_has_required_chapter_learning_structure() -> None:
    lines = _lines()
    chapter_blocks = "\n".join(lines).split("\n# ")
    for block in chapter_blocks:
        if not block.strip():
            continue
        text = "# " + block if not block.startswith("# ") else block
        if "# Chapter " not in text:
            continue
        for required in (
            "## Intro into this chapter",
            "## What you are going to use",
            "## What you will learn in this chapter",
            "## The work, clearly laid out",
            "## Examples of what you might see",
            "## Some explanation",
            "## After you interact: What you learned",
            "## Reflection Questions",
            "## What to Try Next in This Chapter",
        ):
            assert required in text


def test_book_avoids_repeated_boilerplate_in_learning_and_reflection_bullets() -> None:
    lines = _lines()
    chapter = ""
    section = ""
    learned_seen: dict[str, str] = {}
    reflection_seen: dict[str, str] = {}

    for raw in lines:
        stripped = raw.strip()
        if stripped.startswith("# Chapter "):
            chapter = stripped[2:].strip()
            section = ""
            continue
        if stripped.startswith("## "):
            section = stripped[3:].strip().lower()
            continue
        if not stripped.startswith("- "):
            continue
        bullet = stripped[2:].strip().lower()
        if section.startswith("after you interact: what you learned"):
            prior = learned_seen.get(bullet)
            assert not prior or prior == chapter
            learned_seen[bullet] = chapter
        if section.startswith("reflection questions"):
            prior = reflection_seen.get(bullet)
            assert not prior or prior == chapter
            reflection_seen[bullet] = chapter


def test_book_images_have_alt_text_and_caption() -> None:
    lines = _lines()
    image_line_re = re.compile(r"^!\[(.*?)\]\((.*?)\)$")

    for idx, raw in enumerate(lines):
        stripped = raw.strip()
        match = image_line_re.match(stripped)
        if not match:
            continue
        alt_text = match.group(1).strip()
        assert len(alt_text) >= 8
        caption_found = False
        for probe in range(idx + 1, min(len(lines), idx + 5)):
            candidate = lines[probe].strip()
            if not candidate:
                continue
            caption_found = candidate.lower().startswith("caption:")
            break
        assert caption_found


def test_book_intro_sections_have_minimum_depth() -> None:
    lines = _lines()
    chapter = ""
    in_intro = False
    intro_words = 0
    intro_counts: dict[str, int] = {}

    for raw in lines:
        stripped = raw.strip()
        if stripped.startswith("# "):
            if chapter.startswith("Chapter "):
                intro_counts[chapter] = intro_words
            chapter = stripped[2:].strip()
            in_intro = False
            intro_words = 0
            continue
        if stripped.startswith("## "):
            in_intro = stripped[3:].strip().lower() == "intro into this chapter"
            continue
        if not in_intro or not stripped or stripped.startswith("![") or stripped.startswith("Caption:"):
            continue
        intro_words += len(stripped.split())

    if chapter.startswith("Chapter "):
        intro_counts[chapter] = intro_words

    assert intro_counts
    assert all(count >= 28 for count in intro_counts.values())


def test_book_includes_apa_references_section() -> None:
    text = BOOK_MD.read_text(encoding="utf-8")
    assert "## References (APA 7th Edition)" in text
