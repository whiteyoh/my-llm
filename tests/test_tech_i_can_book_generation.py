from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load_book_module():
    module_path = Path("tools/pdf/generate_tech_i_can_book.py")
    spec = importlib.util.spec_from_file_location("tech_i_can_book", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load book generator module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pdf_extra_declares_book_dependencies() -> None:
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8").lower()
    assert "[project.optional-dependencies]" in pyproject
    assert "pdf = [" in pyproject
    for dep in ("reportlab", "pillow", "pypdf"):
        assert dep in pyproject, f"Expected '{dep}' in pdf optional dependencies"


def test_book_render_is_deterministic_for_same_input(tmp_path: Path) -> None:
    try:
        module = _load_book_module()
    except SystemExit:
        pytest.skip('book PDF dependencies not installed; run: pip install -e ".[dev,pdf]"')

    module._build_mod_date = lambda: "D:20260501000000Z"  # type: ignore[method-assign]

    first_pdf = tmp_path / "book_first.pdf"
    second_pdf = tmp_path / "book_second.pdf"
    module.render_book(first_pdf)
    module.render_book(second_pdf)

    assert first_pdf.read_bytes() == second_pdf.read_bytes()


def test_book_render_contains_required_front_and_back_matter(tmp_path: Path) -> None:
    try:
        module = _load_book_module()
    except SystemExit:
        pytest.skip('book PDF dependencies not installed; run: pip install -e ".[dev,pdf]"')

    out_pdf = tmp_path / "book.pdf"
    module.render_book(out_pdf)
    reader = module.PdfReader(str(out_pdf))
    text = "\n".join((page.extract_text() or "") for page in reader.pages)

    for required in (
        "Preface",
        "Chapter 42: Conclusion",
        "Chapter 43: About the Author",
        "Chapter 44: Key Words Index",
        "Dedicated to all of the budding techies of the future.",
        "The world is ready for your brilliance.",
        "Curious today, Confident tomorrow.",
        "Snippet Type: Bash",
        "Snippet Type: Text Output",
    ):
        assert required in text, f"Missing expected book content: {required}"

    assert "Series tagline:" not in text


def test_book_render_stays_under_size_budget(tmp_path: Path) -> None:
    try:
        module = _load_book_module()
    except SystemExit:
        pytest.skip('book PDF dependencies not installed; run: pip install -e ".[dev,pdf]"')

    out_pdf = tmp_path / "book.pdf"
    module.render_book(out_pdf)
    assert out_pdf.stat().st_size <= module.TARGET_PDF_SIZE_BYTES


def test_book_pipeline_avoids_utcnow_deprecation_path() -> None:
    source = Path("tools/pdf/generate_tech_i_can_book.py").read_text(encoding="utf-8")
    assert "datetime.utcnow(" not in source
