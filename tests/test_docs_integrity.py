from pathlib import Path


def test_readme_contains_core_sections_and_links() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "## The idea" in readme
    assert "## Why it exists" in readme
    assert "## What you should see" in readme
    assert "## Learn Mode" in readme
    assert "docs/first_lesson_walkthrough.md" in readme
    assert "docs/teacher_guide.md" in readme
    assert "docs/student_worksheet.md" in readme
    assert "docs/architecture.md" in readme
    assert "docs/how_llms_work.md" in readme


def test_required_docs_and_logo_exist() -> None:
    assert Path("docs/first_lesson_walkthrough.md").exists()
    assert Path("docs/teacher_guide.md").exists()
    assert Path("docs/student_worksheet.md").exists()
    assert Path("docs/architecture.md").exists()
    assert Path("docs/how_llms_work.md").exists()
    assert Path("docs/assets/kairo-logo.svg").exists()


def test_required_content_in_docs() -> None:
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
