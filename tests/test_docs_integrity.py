from pathlib import Path


def test_readme_contains_core_sections_and_links() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

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
        "data/samples/pirate_dialogue.txt",
        "data/samples/sci_fi_micro_story.txt",
        "data/samples/short_poems.txt",
    ]
    for path in required_paths:
        assert Path(path).exists(), f"Missing required path: {path}"


def test_required_content_and_navigation_in_docs() -> None:
    first_lesson = Path("docs/first_lesson_walkthrough.md").read_text(encoding="utf-8")
    teacher = Path("docs/teacher_guide.md").read_text(encoding="utf-8")
    student = Path("docs/student_worksheet.md").read_text(encoding="utf-8")
    architecture = Path("docs/architecture.md").read_text(encoding="utf-8")
    how_llms = Path("docs/how_llms_work.md").read_text(encoding="utf-8")

    assert "# First Lesson Walkthrough" in first_lesson
    assert "## Suggested classroom pacing" in teacher
    assert "# Challenge 1" in student
    assert "## What happens during training?" in architecture
    assert "## What is next-token prediction?" in how_llms
    assert "Before/after retrain exercise prompts" in first_lesson
    assert "## New sample datasets" in student

    for content in (first_lesson, teacher, student, architecture, how_llms):
        assert 'img src="assets/kairo-logo.svg"' in content
        assert "First Lesson Walkthrough" in content
        assert "Teacher Guide" in content
        assert "Student Worksheet" in content
        assert "Architecture" in content
        assert "How LLMs Work" in content
