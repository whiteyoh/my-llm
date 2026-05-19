from pathlib import Path
import re


DOC_FILES = [
    "README.md",
    "docs/first_lesson_walkthrough.md",
    "docs/teacher_guide.md",
    "docs/student_worksheet.md",
    "docs/architecture.md",
    "docs/how_llms_work.md",
]

NAV_LABELS = [
    "Home",
    "First Lesson Walkthrough",
    "Teacher Guide",
    "Student Worksheet",
    "Architecture",
    "How LLMs Work",
]


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_readme_contains_core_sections_and_links() -> None:
    readme = _read("README.md")

    assert "## The idea" in readme
    assert "## Why it exists" in readme
    assert "## What you should see" in readme
    assert "## Learn Mode" in readme
    assert "## Learn Mode screenshots" in readme
    assert "### Printable lesson packs" in readme
    assert "### New sample datasets" in readme
    assert "docs/first_lesson_walkthrough.md" in readme
    assert "docs/teacher_guide.md" in readme
    assert "docs/student_worksheet.md" in readme
    assert "docs/architecture.md" in readme
    assert "docs/how_llms_work.md" in readme
    assert "## The magic moment" in readme


def test_required_docs_assets_and_datasets_exist() -> None:
    required_paths = [
        "docs/first_lesson_walkthrough.md",
        "docs/teacher_guide.md",
        "docs/student_worksheet.md",
        "docs/architecture.md",
        "docs/how_llms_work.md",
        "docs/assets/kairo-logo.svg",
        "docs/assets/simple-architecture-flowchart.svg",
        "docs/assets/learn-mode-token-preview.svg",
        "docs/assets/learn-mode-attention-map.svg",
        "docs/assets/learn-mode-probability-table.svg",
        "docs/assets/learn-mode-retrain-compare.svg",
        "docs/printable/teacher_guide.pdf",
        "docs/printable/student_worksheet.pdf",
        "docs/printable/first_lesson_walkthrough.pdf",
        "tools/pdf/generate_printables.py",
        "tools/pdf/printable.css",
    ]
    for path in required_paths:
        assert Path(path).exists(), f"Missing required path: {path}"

    sample_datasets = [
        "data/samples/pirate_dialogue.txt",
        "data/samples/sci_fi_micro_story.txt",
        "data/samples/short_poems.txt",
        "data/samples/space_adventure.txt",
        "data/samples/nature_notes.txt",
        "data/samples/robot_helper.txt",
    ]
    for dataset in sample_datasets:
        assert Path(dataset).exists(), f"Missing sample dataset: {dataset}"


def test_required_content_and_navigation_in_docs() -> None:
    first_lesson = _read("docs/first_lesson_walkthrough.md")
    teacher = _read("docs/teacher_guide.md")
    student = _read("docs/student_worksheet.md")
    architecture = _read("docs/architecture.md")
    how_llms = _read("docs/how_llms_work.md")

    assert "# First Lesson Walkthrough" in first_lesson
    assert "## Suggested classroom pacing" in teacher
    assert "## Quick-reference classroom flow" in teacher
    assert "# Challenge 1" in student
    assert "## Output before retrain" in student
    assert "## Output after retrain" in student
    assert "## What changed and why?" in student
    assert "## Reflection" in student
    assert "## Extension challenges" in student
    assert "## What happens during training?" in architecture
    assert "## What is next-token prediction?" in how_llms
    assert "Before/after retrain exercise prompts" in first_lesson
    assert "## New sample datasets" in student

    for path in DOC_FILES:
        content = _read(path)
        for label in NAV_LABELS:
            assert label in content, f"Missing nav label '{label}' in {path}"


def test_markdown_links_and_asset_references_are_valid() -> None:
    markdown_link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    image_src_pattern = re.compile(r'<img[^>]+src="([^"]+)"')

    for path in DOC_FILES:
        content = _read(path)
        base_dir = Path(path).parent

        for target in markdown_link_pattern.findall(content):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            link_path = target.split("#", maxsplit=1)[0]
            if not link_path:
                continue
            resolved = (base_dir / link_path).resolve()
            assert resolved.exists(), f"Broken markdown link in {path}: {target}"

        for img_src in image_src_pattern.findall(content):
            resolved = (base_dir / img_src).resolve()
            assert resolved.exists(), f"Broken image source in {path}: {img_src}"


def test_magic_moment_reference_present() -> None:
    readme = _read("README.md")
    assert "magic moment" in readme.lower(), "Missing 'magic moment' reference in README.md"
