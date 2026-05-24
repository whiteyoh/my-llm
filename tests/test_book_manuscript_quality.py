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
            "## About this chapter",
            "## What you are going to use",
            "## What you will learn in this chapter",
            "## The work, clearly laid out",
            "## Examples of what you might see",
            "## Why This Matters",
            "## Action 1: What You Learned",
            "## Action 2: Reflect",
            "## Action 3: Do This Next",
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
        if section.startswith("action 1: what you learned"):
            prior = learned_seen.get(bullet)
            assert not prior or prior == chapter
            learned_seen[bullet] = chapter
        if section.startswith("action 2: reflect"):
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
            in_intro = stripped[3:].strip().lower() == "about this chapter"
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


def test_chapter_next_steps_include_collaboration() -> None:
    text = BOOK_MD.read_text(encoding="utf-8")
    chapter_blocks = re.split(r"\n# Chapter \d+: ", text)[1:]
    collaboration_tokens = (
        "peer",
        "colleague",
        "partner",
        "group",
        "classmate",
        "teacher",
        "swap",
        "pair",
        "pairs",
        "together",
    )

    missing_collab: list[str] = []
    for block in chapter_blocks:
        title = block.splitlines()[0].strip()
        action_match = re.search(r"## Action 3: Do This Next\n(.*?)(\n## |\n---|\Z)", block, flags=re.S)
        assert action_match is not None, f"Missing Action 3 in chapter: {title}"
        bullets = [ln.strip()[2:].strip().lower() for ln in action_match.group(1).splitlines() if ln.strip().startswith("- ")]
        assert len(bullets) >= 2, f"Action 3 needs at least two bullets in chapter: {title}"
        has_collab = any(any(token in bullet for token in collaboration_tokens) for bullet in bullets)
        if not has_collab:
            missing_collab.append(title)

    assert not missing_collab, f"Action 3 missing collaborative task in: {missing_collab}"


def test_book_avoids_repeated_intro_template_phrasing() -> None:
    text = BOOK_MD.read_text(encoding="utf-8")
    banned_phrases = (
        "You are aiming for practical understanding, not just completion.",
        "This chapter takes you through a clear sequence:",
    )
    for phrase in banned_phrases:
        assert phrase not in text


def test_reflection_questions_align_with_taught_content() -> None:
    text = BOOK_MD.read_text(encoding="utf-8")
    chapter_blocks = re.split(r"\n# Chapter \d+: ", text)[1:]

    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "if",
        "then",
        "with",
        "without",
        "for",
        "of",
        "to",
        "in",
        "on",
        "by",
        "from",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "this",
        "that",
        "these",
        "those",
        "your",
        "you",
        "we",
        "they",
        "it",
        "as",
        "at",
        "not",
        "do",
        "does",
        "did",
        "can",
        "could",
        "should",
        "would",
        "will",
        "may",
        "might",
        "which",
        "what",
        "where",
        "when",
        "how",
        "why",
    }

    def _keywords(value: str) -> list[str]:
        tokens = re.findall(r"[A-Za-z][A-Za-z0-9\-']+", value.lower())
        return [token for token in tokens if len(token) > 3 and token not in stop_words]

    failures: list[str] = []
    for block in chapter_blocks:
        chapter_title = block.splitlines()[0].strip()
        reflect_match = re.search(
            r"## Action 2: Reflect\n(.*?)(\n## Action 3: Do This Next|\n---|\Z)",
            block,
            flags=re.S,
        )
        assert reflect_match is not None, f"Missing reflection section in chapter: {chapter_title}"
        reflect_questions = [line.strip()[2:].strip() for line in reflect_match.group(1).splitlines() if line.strip().startswith("- ")]
        assert len(reflect_questions) == 3, f"Expected 3 reflection questions in chapter: {chapter_title}"

        taught_content = block.split("## Action 2: Reflect", 1)[0]
        taught_terms = set(_keywords(taught_content))
        for question in reflect_questions:
            question_terms = _keywords(question)
            if not any(term in taught_terms for term in question_terms):
                failures.append(f"{chapter_title}: {question}")

    assert not failures, "Reflection question not aligned to taught content:\n" + "\n".join(failures)


def test_book_code_snippets_follow_manual_style_rules() -> None:
    lines = _lines()
    code_blocks: list[tuple[int, int, str]] = []
    in_code = False
    start = 0
    lang = ""
    for idx, line in enumerate(lines, start=1):
        if line.startswith("```"):
            if not in_code:
                in_code = True
                start = idx
                lang = line[3:].strip().lower()
            else:
                code_blocks.append((start, idx, lang))
                in_code = False
    assert not in_code

    allowed_languages = {"bash", "sh", "text", "python", "yaml", "json", "sql", "toml"}
    assert all(lang for _start, _end, lang in code_blocks)
    assert all(lang in allowed_languages for _start, _end, lang in code_blocks)

    shell_prompt_lines: list[int] = []
    smart_quote_lines: list[int] = []
    shell_output_markers: list[int] = []
    for start_line, end_line, block_lang in code_blocks:
        block_lines = lines[start_line:end_line - 1]
        for idx, content_line in enumerate(block_lines, start=start_line + 1):
            stripped = content_line.strip()
            if any(ch in content_line for ch in "“”‘’"):
                smart_quote_lines.append(idx)
            if block_lang in {"bash", "sh"} and stripped.startswith("$"):
                shell_prompt_lines.append(idx)
            if block_lang in {"bash", "sh"} and re.match(
                r"^(Generated|Output|Traceback|ERROR|Warning:|Ghostscript|Book PDF is)\b",
                stripped,
            ):
                shell_output_markers.append(idx)
        if block_lang in {"bash", "sh"}:
            context = [lines[i - 1].strip() for i in range(max(1, start_line - 6), start_line)]
            assert any(item.startswith("Snippet Purpose:") for item in context)

    assert not shell_prompt_lines
    assert not smart_quote_lines
    assert not shell_output_markers
