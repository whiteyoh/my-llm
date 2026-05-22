from pathlib import Path
import re


DOC_FILES = [
    "README.md",
    "STEP_BY_STEP.md",
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

REQUIRED_SECTIONS = {
    "README.md": [
        "# Kairo",
        "## Why Kairo?",
        "## The magic moment",
        "## Documentation map",
    ],
    "STEP_BY_STEP.md": [
        "# Kairo Step-by-Step Guide",
        "## 2. Train on normal story text",
        "## 5. Generate with the same prompt",
        "## 8. Print classroom materials",
    ],
    "docs/first_lesson_walkthrough.md": [
        "# First Lesson Walkthrough",
        "## Sample datasets for this lesson",
        "## Step 1 — Train on normal story data",
        "## Step 4 — Generate output after retrain",
        "## What success looks like",
        "Expected style",
        "## Before/after retrain exercise prompts",
    ],
    "docs/teacher_guide.md": [
        "# Teacher Guide",
        "## Quick-reference classroom flow",
        "## Suggested classroom pacing",
        "## Facilitation tips",
        "## Common misconceptions and Q&A guidance",
        "## Teacher gotchas",
        "## Example teacher script",
    ],
    "docs/student_worksheet.md": [
        "# Student Worksheet",
        "### Output Before Retrain",
        "### Output After Retrain",
        "### What Changed and Why?",
        "### Reflection",
        "### Extension exercises",
        "## Final reflection",
    ],
    "docs/architecture.md": [
        "# Architecture",
        "## System diagram",
        "## Normal to pirate retrain flow",
        "## What happens during training?",
    ],
    "docs/how_llms_work.md": [
        "# How LLMs Work (Simple)",
        "## What is next-token prediction?",
        "## What is attention?",
        "## FAQ",
    ],
}


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_required_sections_exist_in_docs() -> None:
    for path, sections in REQUIRED_SECTIONS.items():
        content = _read(path)
        for section in sections:
            assert section in content, f"Missing section '{section}' in {path}"


def test_assets_and_docs_exist_and_are_referenced() -> None:
    required_paths = [
        "docs/assets/kairo-logo.svg",
        "docs/assets/simple-architecture-flowchart.svg",
        "docs/assets/learn-mode-token-preview.svg",
        "docs/assets/learn-mode-attention-map.svg",
        "docs/assets/learn-mode-probability-table.svg",
        "docs/assets/learn-mode-retrain-compare.svg",
        "docs/first_lesson_walkthrough.md",
        "docs/teacher_guide.md",
        "docs/student_worksheet.md",
        "docs/architecture.md",
        "docs/how_llms_work.md",
        "docs/printable/teacher_guide.pdf",
        "docs/printable/student_worksheet.pdf",
        "docs/printable/first_lesson_walkthrough.pdf",
        "docs/printable/Kairo_Teacher_Guide.pdf",
        "docs/printable/Kairo_Student_Worksheet.pdf",
        "docs/printable/Kairo_First_Lesson_Walkthrough.pdf",
    ]
    for path in required_paths:
        assert Path(path).exists(), f"Missing required path: {path}"

    readme = _read("README.md")
    for asset in [
        "docs/assets/kairo-logo.svg",
        "docs/assets/simple-architecture-flowchart.svg",
        "docs/assets/learn-mode-token-preview.svg",
        "docs/assets/learn-mode-attention-map.svg",
        "docs/assets/learn-mode-probability-table.svg",
        "docs/assets/learn-mode-retrain-compare.svg",
    ]:
        assert asset in readme, f"README missing asset reference: {asset}"


def test_top_and_footer_navigation_present() -> None:
    for path in DOC_FILES:
        if path == "STEP_BY_STEP.md":
            continue
        content = _read(path)
        for label in NAV_LABELS:
            assert label in content, f"Missing nav label '{label}' in {path}"

        assert content.count('<p align="center">') >= 2, (
            f"Expected top and footer navigation blocks in {path}"
        )


def test_markdown_links_and_image_src_are_valid() -> None:
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


def test_printable_pdfs_are_committed_and_readable() -> None:
    pdfs = [
        "docs/printable/teacher_guide.pdf",
        "docs/printable/student_worksheet.pdf",
        "docs/printable/first_lesson_walkthrough.pdf",
        "docs/printable/Kairo_Teacher_Guide.pdf",
        "docs/printable/Kairo_Student_Worksheet.pdf",
        "docs/printable/Kairo_First_Lesson_Walkthrough.pdf",
    ]

    for path in pdfs:
        data = Path(path).read_bytes()
        assert data.startswith(b"%PDF-"), f"Printable is not a PDF: {path}"
        assert len(data) > 1_000, f"Printable looks unexpectedly small: {path}"


def test_printable_pdf_aliases_match_primary_files() -> None:
    aliases = {
        "docs/printable/teacher_guide.pdf": "docs/printable/Kairo_Teacher_Guide.pdf",
        "docs/printable/student_worksheet.pdf": "docs/printable/Kairo_Student_Worksheet.pdf",
        "docs/printable/first_lesson_walkthrough.pdf": (
            "docs/printable/Kairo_First_Lesson_Walkthrough.pdf"
        ),
    }

    for primary, alias in aliases.items():
        assert Path(primary).read_bytes() == Path(alias).read_bytes(), (
            f"Printable alias differs from primary file: {alias}"
        )
