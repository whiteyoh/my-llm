from pathlib import Path


def _shared_header() -> str:
    return (
        '<p align="center">\n'
        '  <img src="assets/kairo-logo.svg" alt="Kairo logo" width="640"/>\n'
        '</p>\n\n'
        '<p align="center">\n'
        '  <a href="../README.md">Home</a> •\n'
        '  <a href="teacher_guide.md">Teacher Guide</a> •\n'
        '  <a href="student_worksheet.md">Student Worksheet</a> •\n'
        '  <a href="architecture.md">Architecture</a> •\n'
        '  <a href="how_llms_work.md">How LLMs Work</a>\n'
        '</p>\n\n'
        '---\n'
    )


def test_readme_contains_core_sections_and_links() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "## What you should see" in readme
    assert "## Learn Mode" in readme
    assert "(docs/teacher_guide.md)" in readme
    assert "(docs/student_worksheet.md)" in readme
    assert "(docs/architecture.md)" in readme
    assert "(docs/how_llms_work.md)" in readme


def test_docs_have_shared_header_block() -> None:
    header = _shared_header()
    for doc_path in Path("docs").glob("*.md"):
        contents = doc_path.read_text(encoding="utf-8")
        assert contents.startswith(header), f"Missing shared header in {doc_path}"


def test_teacher_guide_core_sections_present() -> None:
    teacher = Path("docs/teacher_guide.md").read_text(encoding="utf-8")
    assert "## Suggested classroom pacing" in teacher
    assert "## Troubleshooting" in teacher


def test_student_architecture_and_how_llms_sections_present() -> None:
    student = Path("docs/student_worksheet.md").read_text(encoding="utf-8")
    architecture = Path("docs/architecture.md").read_text(encoding="utf-8")
    how_llms = Path("docs/how_llms_work.md").read_text(encoding="utf-8")

    assert "# Challenge 1" in student
    assert "## What happens during training?" in architecture
    assert "## What is next-token prediction?" in how_llms


def test_logo_asset_exists() -> None:
    assert Path("docs/assets/kairo-logo.svg").exists()
