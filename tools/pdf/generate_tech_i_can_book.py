from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from html import escape
from pathlib import Path
import re
import shutil
import subprocess
import textwrap

try:
    from PIL import Image as PILImage
    from PIL import ImageDraw, ImageFont
    from PIL import ImageFilter
    from reportlab import rl_config
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfdoc
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        Image,
        KeepTogether,
        NextPageTemplate,
        PageBreak,
        PageTemplate,
        Paragraph,
        Preformatted,
        Spacer,
        Table,
        TableStyle,
    )
    from reportlab.platypus.tableofcontents import TableOfContents
    from pypdf import PdfReader
    from pypdf import PdfWriter
    from pypdf.generic import BooleanObject, DictionaryObject, NameObject, TextStringObject
except Exception as exc:  # pragma: no cover
    raise SystemExit("Missing PDF tooling. Install with: pip install -e \".[pdf]\"") from exc


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
PRINTABLE = DOCS / "printable"
BOOK_MD = DOCS / "tech_i_can_kairo_book.md"
BOOK_PDF = PRINTABLE / "Tech_I_Can_Kairo_Book.pdf"
COVER_IMAGE = ASSETS / "tech-i-can-cover.png"

BOOK_TITLE = "Tech I Can"
BOOK_TAGLINE = "Curious today, Confident tomorrow"
BOOK_SUBTITLE = "Kairo: A Beginner-Friendly Guide to Building and Understanding Tiny Language Models"
BOOK_AUTHOR = "Paul McMurray"
BOOK_EDITION = "Classroom Edition (2026)"
BOOK_SERIES = "Tech I Can Series"
BOOK_PUBLISHER = "Tech I Can"
BOOK_PUBLICATION_DATE = "May 2026"
BOOK_ISBN = "ISBN: Not assigned (Edition 1 school release, not for retail sale)"
BOOK_KEYWORDS = "education, ai literacy, tiny llm, classroom, kairo, beginner ai"
BRAND_ACCENTS = ["#2563eb", "#0d9488", "#ea580c", "#7c3aed", "#0891b2", "#be123c"]
BOOK_META_TITLE = "Tech I Can | Kairo"
BOOK_META_AUTHOR = "Paul McMurray"
BOOK_META_SUBJECT = "Beginner guide to Kairo"
BOOK_META_CREATOR = "Tech I Can Production Pipeline"
BOOK_META_CREATION_DATE = "2026-05-01T00:00:00+00:00"


def _build_mod_date() -> str:
    return datetime.utcnow().strftime("D:%Y%m%d%H%M%SZ")


def apply_accessibility_catalog_tags(pdf_path: Path) -> None:
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer._root_object.update(  # type: ignore[attr-defined]
        {
            NameObject("/MarkInfo"): DictionaryObject({NameObject("/Marked"): BooleanObject(True)}),
            NameObject("/Lang"): TextStringObject("en-GB"),
        }
    )
    tagged_path = pdf_path.with_name(f"{pdf_path.stem}.tagged{pdf_path.suffix}")
    with tagged_path.open("wb") as handle:
        writer.write(handle)
    tagged_path.replace(pdf_path)


def optimise_pdf_with_ghostscript(pdf_path: Path) -> bool:
    gs_path = shutil.which("gs")
    if not gs_path:
        print("Ghostscript not found; skipping PDF optimisation step.")
        return False

    optimised_path = pdf_path.with_name(f"{pdf_path.stem}.optimised{pdf_path.suffix}")
    cmd = [
        gs_path,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={optimised_path}",
        str(pdf_path),
    ]
    subprocess.run(cmd, check=True)
    optimised_path.replace(pdf_path)
    return True

rl_config.invariant = 1
PAGE_TOTAL_HINT = 0


class BookPDFInfo(pdfdoc.PDFInfo):
    def format(self, document):  # type: ignore[override]
        data = {
            "Title": pdfdoc.PDFString(self.title),
            "Author": pdfdoc.PDFString(self.author),
            "Subject": pdfdoc.PDFString(self.subject),
            "Creator": pdfdoc.PDFString(self.creator),
            "Producer": pdfdoc.PDFString(self.producer),
            "Keywords": pdfdoc.PDFString(self.keywords),
            "CreationDate": pdfdoc.PDFString(BOOK_META_CREATION_DATE),
            "ModDate": pdfdoc.PDFString(_build_mod_date()),
            "Trapped": pdfdoc.PDFName(self.trapped),
        }
        return pdfdoc.PDFDictionary(data).format(document)


class DeterministicCanvas(Canvas):
    last_page_count = 0

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("invariant", 1)
        super().__init__(*args, **kwargs)
        self._doc.info = BookPDFInfo()
        self.setTitle(BOOK_META_TITLE)
        self.setAuthor(BOOK_META_AUTHOR)
        self.setSubject(BOOK_META_SUBJECT)
        self.setCreator(BOOK_META_CREATOR)
        self.setKeywords(BOOK_KEYWORDS)

    def save(self):  # type: ignore[override]
        # ReportLab's final page index can be one step ahead at save-time.
        DeterministicCanvas.last_page_count = max(0, self.getPageNumber() - 1)
        super().save()


class BookDocTemplate(BaseDocTemplate):
    def afterFlowable(self, flowable):  # type: ignore[no-untyped-def]
        level = getattr(flowable, "_toc_level", None)
        text = getattr(flowable, "_toc_text", None)
        if level is not None and text:
            self.notify("TOCEntry", (int(level), text, self.page))
        chapter_marker = getattr(flowable, "_running_chapter", None)
        section_marker = getattr(flowable, "_running_section", None)
        if chapter_marker:
            self.current_running_chapter = chapter_marker
        chapter_accent = getattr(flowable, "_chapter_accent", None)
        if chapter_accent:
            self.current_chapter_accent = chapter_accent
        if section_marker:
            self.current_running_section = section_marker


def ensure_cover_image(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = 2480, 3508
    image = PILImage.new("RGB", (width, height), "#050b18")
    draw = ImageDraw.Draw(image)

    # Base vertical gradient.
    for y in range(height):
        ratio = y / max(1, height - 1)
        r = int(5 + (20 - 5) * ratio)
        g = int(11 + (34 - 11) * ratio)
        b = int(24 + (66 - 24) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Diagonal sheen overlay.
    sheen = PILImage.new("RGBA", (width, height), (0, 0, 0, 0))
    sheen_draw = ImageDraw.Draw(sheen, "RGBA")
    for i in range(-height, width, 120):
        sheen_draw.line(
            [(i, 0), (i + height, height)],
            fill=(255, 255, 255, 22),
            width=2,
        )
    sheen = sheen.filter(ImageFilter.GaussianBlur(1.2))

    # Soft glow shapes for depth.
    glow = PILImage.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow, "RGBA")
    glow_draw.ellipse((-380, -120, 1120, 1280), fill=(56, 189, 248, 120))
    glow_draw.ellipse((1320, 120, 2860, 1580), fill=(16, 185, 129, 115))
    glow_draw.ellipse((640, 2550, 2420, 4300), fill=(59, 130, 246, 140))
    glow = glow.filter(ImageFilter.GaussianBlur(28))

    composed = PILImage.alpha_composite(image.convert("RGBA"), glow)
    composed = PILImage.alpha_composite(composed, sheen)

    # Text area panel for cleaner readability.
    panel = PILImage.new("RGBA", (width, height), (0, 0, 0, 0))
    panel_draw = ImageDraw.Draw(panel, "RGBA")
    panel_draw.rounded_rectangle(
        (210, 1500, 2260, 2920),
        radius=34,
        fill=(8, 17, 40, 125),
        outline=(255, 255, 255, 48),
        width=2,
    )
    panel_draw.rectangle((280, 1530, 2140, 1600), fill=(245, 158, 11, 240))
    panel_draw.rectangle((280, 2790, 2140, 2830), fill=(148, 163, 184, 230))
    composed = PILImage.alpha_composite(composed, panel)
    image = composed.convert("RGB")

    def load_font(size: int) -> ImageFont.ImageFont:
        candidates = [
            "/System/Library/Fonts/Supplemental/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size=size)
            except OSError:
                continue
        return ImageFont.load_default()

    draw = ImageDraw.Draw(image)
    title_font = load_font(206)
    chapter_font = load_font(132)
    tag_font = load_font(66)
    subtitle_font = load_font(52)
    meta_font = load_font(44)
    strip_font = load_font(44)
    author_font = load_font(64)

    def draw_centered_text(text: str, font: ImageFont.ImageFont, y: int, fill: tuple[int, int, int]) -> None:
        left, right = 280, 2140
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        x = int(left + ((right - left - width) / 2))
        draw.text((x, y), text, fill=fill, font=font)

    draw.text((280, 1688), "TECH I CAN", fill=(249, 250, 251), font=title_font)
    draw.text((280, 1868), "Kairo", fill=(251, 191, 36), font=chapter_font)
    draw.text((280, 2070), BOOK_TAGLINE, fill=(224, 231, 255), font=tag_font)
    draw.text((280, 2230), "A practical beginner guide to tiny language models", fill=(226, 232, 240), font=subtitle_font)
    draw.text((280, 2472), BOOK_EDITION, fill=(177, 194, 214), font=meta_font)
    draw.text((280, 2550), BOOK_SERIES, fill=(170, 186, 205), font=meta_font)
    draw.text((280, 2630), f"By {BOOK_AUTHOR}", fill=(241, 245, 249), font=author_font)
    draw_centered_text("Build. Train. Compare. Explain.", strip_font, 2732, (227, 235, 246))

    image.save(path, format="PNG")


def clean_lines(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "---":
            continue
        lines.append(line.rstrip())
    return lines


def validate_book_structure(lines: list[str]) -> None:
    text = "\n".join(lines)
    if "# Chapter 41: Glossary (Terms and Parameters)" not in text:
        raise SystemExit("Book markdown is missing the glossary chapter heading.")
    if "# Chapter 44: Key Words Index" not in text:
        raise SystemExit("Book markdown is missing the key words index chapter heading.")

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
    if in_code:
        raise SystemExit("Book markdown has an unclosed fenced code block.")

    missing_snippet: list[int] = []
    for start_line, _end, block_lang in code_blocks:
        if block_lang not in {"bash", "sh"}:
            continue
        context = [lines[i - 1].strip() for i in range(max(1, start_line - 6), start_line)]
        if not any(item.startswith("Snippet Purpose:") for item in context):
            missing_snippet.append(start_line)
    if missing_snippet:
        raise SystemExit(f"Missing 'Snippet Purpose:' before bash block lines: {missing_snippet}")

    glossary_index = next((i for i, line in enumerate(lines) if line.startswith("# Chapter 41: Glossary")), -1)
    if glossary_index < 0:
        raise SystemExit("Could not find glossary chapter for parameter validation.")
    keyword_index_start = next((i for i, line in enumerate(lines) if line.startswith("# Chapter 44: Key Words Index")), -1)
    glossary_slice_end = keyword_index_start if keyword_index_start > glossary_index else len(lines)
    glossary_text = "\n".join(lines[glossary_index:glossary_slice_end])
    all_params = set(re.findall(r"--[a-zA-Z0-9_]+", text))
    glossary_params = set(re.findall(r"\*\*`(--[a-zA-Z0-9_]+)`\*\*", glossary_text))
    missing_glossary_params = sorted(param for param in all_params if param not in glossary_params)
    if missing_glossary_params:
        raise SystemExit(
            f"Parameter(s) used in manuscript but missing from glossary: {missing_glossary_params}"
        )


def extract_keyword_terms(lines: list[str]) -> list[str]:
    terms: list[str] = []
    in_glossary = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# Chapter 41: Glossary"):
            in_glossary = True
            continue
        if in_glossary and stripped.startswith("# Chapter 44: Key Words Index"):
            break
        if not in_glossary or not stripped.startswith("- **"):
            continue
        match = re.match(r"^- \*\*`?([^*`]+?)`?\*\*:", stripped)
        if not match:
            continue
        term = match.group(1).strip()
        if term and term not in terms:
            terms.append(term)
    return terms


def find_heading_page(reader: PdfReader, heading: str) -> int | None:
    needle = heading.lower()
    for idx, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").lower()
        if needle in text:
            return idx
    return None


def build_keyword_page_map(pdf_path: Path, terms: list[str]) -> dict[str, list[int]]:
    reader = PdfReader(str(pdf_path))
    index_page = find_heading_page(reader, "Chapter 44: Key Words Index")
    max_page = (index_page - 1) if index_page else len(reader.pages)
    page_text: list[str] = []
    for page_no in range(1, max_page + 1):
        page = reader.pages[page_no - 1]
        page_text.append((page.extract_text() or "").lower())

    page_map: dict[str, list[int]] = defaultdict(list)
    for term in terms:
        needle = term.lower()
        for page_no, text in enumerate(page_text, start=1):
            if needle in text:
                page_map[term].append(page_no)
    return dict(page_map)


def inline_markup(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    return text


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def chapter_accent_for_heading(heading: str) -> str:
    match = re.match(r"^Chapter\s+(\d+):", heading, flags=re.IGNORECASE)
    if not match:
        return BRAND_ACCENTS[0]
    chapter_no = int(match.group(1))
    return BRAND_ACCENTS[(chapter_no - 1) % len(BRAND_ACCENTS)]


def tint(color_hex: str, amount: float = 0.85) -> colors.Color:
    base = colors.HexColor(color_hex)
    amt = min(1.0, max(0.0, amount))
    return colors.Color(
        base.red + (1 - base.red) * amt,
        base.green + (1 - base.green) * amt,
        base.blue + (1 - base.blue) * amt,
    )


def wrap_code_lines(lines: list[str], width: int = 74) -> str:
    wrapped: list[str] = []
    for line in lines:
        if not line:
            wrapped.append("")
            continue
        indent_len = len(line) - len(line.lstrip(" "))
        indent = line[:indent_len]
        body = line[indent_len:]
        available = max(24, width - indent_len)
        parts = textwrap.wrap(body, width=available, break_long_words=False, break_on_hyphens=False)
        if not parts:
            wrapped.append(line)
            continue
        wrapped.append(indent + parts[0])
        continuation_indent = indent + "  "
        wrapped.extend(continuation_indent + part for part in parts[1:])
    return "\n".join(wrapped)


def merge_callout_continuations(lines: list[str]) -> list[str]:
    merged: list[str] = []
    i = 0
    callout_pattern = re.compile(
        r"^(Lightbulb Takeaway|Definition|Note|Snippet Purpose|Snippet Change):\s*(.*)$",
        flags=re.IGNORECASE,
    )
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        match = callout_pattern.match(stripped)
        if not match:
            merged.append(line)
            i += 1
            continue

        label = match.group(1).strip()
        message_parts = [match.group(2).strip()] if match.group(2).strip() else []
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt:
                break
            if (
                nxt.startswith(("```", "- ", "# ", "## ", "### ", "|"))
                or re.match(r"^\d+\.\s+", nxt)
                or callout_pattern.match(nxt)
            ):
                break
            message_parts.append(nxt)
            i += 1
        message = " ".join(message_parts).strip()
        merged.append(f"{label}: {message}" if message else f"{label}:")
    return merged


def pick_primary_pages(pages: list[int], max_items: int = 5) -> list[int]:
    if not pages:
        return []
    if len(pages) <= max_items:
        return pages
    anchors = [0, len(pages) // 4, len(pages) // 2, (3 * len(pages)) // 4, len(pages) - 1]
    chosen: list[int] = []
    for idx in anchors:
        page = pages[idx]
        if page not in chosen:
            chosen.append(page)
        if len(chosen) >= max_items:
            break
    return chosen


def _page_ranges(pages: list[int]) -> list[tuple[int, int]]:
    if not pages:
        return []
    ranges: list[tuple[int, int]] = []
    start = prev = pages[0]
    for page in pages[1:]:
        if page == prev + 1:
            prev = page
            continue
        ranges.append((start, prev))
        start = prev = page
    ranges.append((start, prev))
    return ranges


def format_page_ranges(pages: list[int], max_ranges: int | None = None) -> str:
    if not pages:
        return "not found"
    ranges = _page_ranges(pages)
    truncated = False
    if max_ranges is not None and len(ranges) > max_ranges:
        ranges = ranges[:max_ranges]
        truncated = True

    rendered: list[str] = []
    for start, end in ranges:
        rendered.append(str(start) if start == end else f"{start}-{end}")
    joined = ", ".join(rendered)
    return f"{joined}, ..." if truncated else joined


def callout_icon(label: str) -> str:
    lookup = {
        "lightbulb takeaway": "✦",
        "definition": "◆",
        "note": "▣",
        "snippet purpose": "⌘",
        "snippet change": "↺",
    }
    return lookup.get(label.lower(), "•")


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    flow_control = {
        "allowOrphans": 0,
        "allowWidows": 0,
        "splitLongWords": 0,
    }
    return {
        "book_title": ParagraphStyle(
            "BookTitle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=30,
            leading=34,
            alignment=1,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=10,
            **flow_control,
        ),
        "book_subtitle": ParagraphStyle(
            "BookSubtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=13,
            leading=18,
            alignment=1,
            textColor=colors.HexColor("#334155"),
            spaceAfter=6,
            **flow_control,
        ),
        "book_tag": ParagraphStyle(
            "BookTag",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=12,
            leading=16,
            alignment=1,
            textColor=colors.HexColor("#0f766e"),
            spaceAfter=14,
            **flow_control,
        ),
        "book_meta": ParagraphStyle(
            "BookMeta",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            alignment=1,
            textColor=colors.HexColor("#475569"),
            spaceAfter=8,
            **flow_control,
        ),
        "running_header": ParagraphStyle(
            "RunningHeader",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=11,
            alignment=0,
            textColor=colors.HexColor("#334155"),
            spaceAfter=0,
            **flow_control,
        ),
        "dedication": ParagraphStyle(
            "Dedication",
            parent=base["BodyText"],
            fontName="Times-Italic",
            fontSize=18,
            leading=28,
            alignment=1,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=10,
            **flow_control,
        ),
        "toc_title": ParagraphStyle(
            "TocTitle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#111827"),
            spaceAfter=12,
            **flow_control,
        ),
        "toc_item": ParagraphStyle(
            "TocItem",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#1f2937"),
            leftIndent=8,
            spaceAfter=2,
            **flow_control,
        ),
        "copyright": ParagraphStyle(
            "Copyright",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=10.5,
            leading=16,
            alignment=4,
            textColor=colors.HexColor("#334155"),
            spaceAfter=8,
            **flow_control,
        ),
        "imprint": ParagraphStyle(
            "Imprint",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            alignment=0,
            textColor=colors.HexColor("#1f2937"),
            spaceAfter=4,
            **flow_control,
        ),
        "chapter": ParagraphStyle(
            "ChapterTitle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=12,
            spaceAfter=10,
            **flow_control,
        ),
        "section": ParagraphStyle(
            "SectionTitle",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=8,
            spaceAfter=5,
            **flow_control,
        ),
        "takeaway_box": ParagraphStyle(
            "TakeawayBox",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=16,
            textColor=colors.HexColor("#7c2d12"),
            backColor=colors.HexColor("#fef3c7"),
            borderColor=colors.HexColor("#f59e0b"),
            borderWidth=0.8,
            borderPadding=6,
            borderRadius=4,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=1,
            **flow_control,
        ),
        "definition_box": ParagraphStyle(
            "DefinitionBox",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=16,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#e2e8f0"),
            borderColor=colors.HexColor("#64748b"),
            borderWidth=0.8,
            borderPadding=6,
            borderRadius=2,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=8,
            spaceAfter=6,
            keepWithNext=1,
            **flow_control,
        ),
        "note_box": ParagraphStyle(
            "NoteBox",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=16,
            textColor=colors.HexColor("#0f172a"),
            backColor=colors.HexColor("#f8fafc"),
            borderColor=colors.HexColor("#94a3b8"),
            borderWidth=0.8,
            borderPadding=6,
            borderRadius=2,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=8,
            spaceAfter=6,
            keepWithNext=1,
            **flow_control,
        ),
        "snippet_box": ParagraphStyle(
            "SnippetBox",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=16,
            textColor=colors.HexColor("#1e3a8a"),
            backColor=colors.HexColor("#dbeafe"),
            borderColor=colors.HexColor("#3b82f6"),
            borderWidth=0.8,
            borderPadding=6,
            borderRadius=2,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=8,
            spaceAfter=5,
            keepWithNext=1,
            **flow_control,
        ),
        "success_box": ParagraphStyle(
            "SuccessBox",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=16,
            textColor=colors.HexColor("#14532d"),
            backColor=colors.HexColor("#dcfce7"),
            borderColor=colors.HexColor("#22c55e"),
            borderWidth=0.8,
            borderPadding=6,
            borderRadius=2,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=8,
            spaceAfter=6,
            keepWithNext=1,
            **flow_control,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=12.1,
            leading=18.4,
            alignment=4,
            textColor=colors.HexColor("#111827"),
            spaceAfter=6,
            **flow_control,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=11.9,
            leading=17.7,
            leftIndent=16,
            bulletIndent=4,
            textColor=colors.HexColor("#111827"),
            spaceAfter=3,
            **flow_control,
        ),
        "learned_detail": ParagraphStyle(
            "LearnedDetail",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=11.6,
            leading=17.1,
            leftIndent=16,
            bulletIndent=4,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=4,
            **flow_control,
        ),
        "code": ParagraphStyle(
            "Code",
            fontName="Courier",
            fontSize=9.6,
            leading=13.0,
            textColor=colors.HexColor("#020617"),
            backColor=colors.HexColor("#f1f5f9"),
            borderColor=colors.HexColor("#94a3b8"),
            borderWidth=0.6,
            borderPadding=7,
            leftIndent=1,
            rightIndent=1,
            spaceBefore=4,
            spaceAfter=9,
            **flow_control,
        ),
        "index_entry": ParagraphStyle(
            "IndexEntry",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=10.8,
            leading=15,
            leftIndent=16,
            bulletIndent=4,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=3,
            **flow_control,
        ),
        "cell": ParagraphStyle(
            "Cell",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=11.2,
            **flow_control,
        ),
        "toc_level_0": ParagraphStyle(
            "TocLevel0",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#111827"),
            leftIndent=8,
            firstLineIndent=0,
            spaceBefore=2,
            spaceAfter=2,
            **flow_control,
        ),
        "toc_level_1": ParagraphStyle(
            "TocLevel1",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#334155"),
            leftIndent=20,
            firstLineIndent=0,
            spaceBefore=1,
            spaceAfter=1,
            **flow_control,
        ),
    }


def append_table(story: list[object], rows: list[str], styles: dict[str, ParagraphStyle], width: float) -> None:
    table_rows: list[list[Paragraph]] = []
    for row in rows:
        if is_table_separator(row):
            continue
        table_rows.append([Paragraph(inline_markup(cell), styles["cell"]) for cell in split_table_row(row)])
    if not table_rows:
        return

    cols = max(len(r) for r in table_rows)
    for row in table_rows:
        while len(row) < cols:
            row.append(Paragraph("", styles["cell"]))

    table = Table(table_rows, colWidths=[width / cols] * cols, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.extend([table, Spacer(1, 8)])


def append_chapter_band(story: list[object], width: float, accent_hex: str) -> None:
    band_w = min(width * 0.36, 64 * mm)
    band = Table([[""]], colWidths=[band_w], rowHeights=[2.6 * mm], hAlign="LEFT")
    band.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(accent_hex)),
                ("LINEBELOW", (0, 0), (-1, -1), 0, colors.white),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(band)
    story.append(Spacer(1, 3))


def chapter_toc_title(chapter_heading: str) -> str:
    if chapter_heading == "How to Use This Book":
        return chapter_heading
    match = re.match(r"^Chapter\s+\d+:\s+(.*)$", chapter_heading, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return chapter_heading.strip()


def build_body_story(
    lines: list[str],
    styles: dict[str, ParagraphStyle],
    width: float,
    keyword_page_map: dict[str, list[int]] | None = None,
) -> list[object]:
    lines = merge_callout_continuations(lines)
    story: list[object] = []
    paragraph: list[str] = []
    code: list[str] = []
    table: list[str] = []
    in_code = False
    # Skip manuscript title preamble; start rendering from the first front-matter section.
    in_body = False
    first_heading = True
    in_after_learning = False
    current_chapter_title = ""
    learned_points = 0
    has_custom_reflection = False
    has_custom_try_next = False

    def flush_paragraph() -> None:
        if paragraph:
            story.append(Paragraph(inline_markup(" ".join(paragraph).strip()), styles["body"]))
            paragraph.clear()

    def flush_code() -> None:
        if code:
            story.append(Preformatted(wrap_code_lines(code), styles["code"]))
            code.clear()

    def flush_table() -> None:
        if table:
            append_table(story, table, styles, width)
            table.clear()

    def append_recap_extensions() -> None:
        nonlocal in_after_learning, learned_points, has_custom_reflection, has_custom_try_next
        if not in_after_learning or learned_points == 0:
            in_after_learning = False
            learned_points = 0
            has_custom_reflection = False
            has_custom_try_next = False
            return

        chapter_ref = current_chapter_title or "this chapter"
        if not has_custom_reflection:
            story.append(Paragraph("Reflection Questions", styles["section"]))
            story.append(
                Paragraph(
                    inline_markup(f"What changed in {chapter_ref}, and which exact output lines prove your claim?"),
                    styles["bullet"],
                    bulletText="•",
                )
            )
            story.append(
                Paragraph(
                    inline_markup("What part was most difficult, and what evidence helped you understand it?"),
                    styles["bullet"],
                    bulletText="•",
                )
            )
            story.append(
                Paragraph(
                    inline_markup("How would you explain this chapter to someone with no coding background?"),
                    styles["bullet"],
                    bulletText="•",
                )
            )
        if not has_custom_try_next:
            story.append(Paragraph("What to Try Next in This Chapter", styles["section"]))
            story.append(
                Paragraph(
                    inline_markup("Re-run one command with a small controlled setting change and compare outcomes."),
                    styles["bullet"],
                    bulletText="•",
                )
            )
            story.append(
                Paragraph(
                    inline_markup("Try one additional prompt and check whether your conclusion still holds."),
                    styles["bullet"],
                    bulletText="•",
                )
            )
        story.append(Spacer(1, 4))
        in_after_learning = False
        learned_points = 0
        has_custom_reflection = False
        has_custom_try_next = False

    def append_keyword_index() -> None:
        entries = keyword_page_map or {}
        if not entries:
            story.append(
                Paragraph(
                    inline_markup("Keyword pages will appear after the first render pass."),
                    styles["note_box"],
                )
            )
            return
        story.append(
            Paragraph(
                inline_markup("Use this index to jump quickly to where each term is taught."),
                styles["note_box"],
            )
        )
        story.append(
            Paragraph(
                inline_markup(
                    "Format: primary pages show the best starting points; full references show complete page ranges."
                ),
                styles["imprint"],
            )
        )
        for term in sorted(entries, key=lambda item: item.lower()):
            pages = entries[term]
            if pages:
                primary = ", ".join(str(page) for page in pick_primary_pages(pages))
                full = format_page_ranges(pages, max_ranges=8)
                page_list = f"Primary: {primary} | Full: {full}"
            else:
                page_list = "not found"
            story.append(Paragraph(inline_markup(f"{term}: {page_list}"), styles["index_entry"], bulletText="•"))

    for line in lines:
        stripped = line.strip()

        if not in_body:
            if (
                stripped.startswith("# Preface")
                or stripped.startswith("# How to Use This Book")
                or stripped.startswith("# Chapter ")
            ):
                in_body = True
            else:
                continue

        if not stripped:
            flush_paragraph()
            story.append(Spacer(1, 5))
            continue

        callout_match = re.match(
            r"^(Lightbulb Takeaway|Definition|Note|Snippet Purpose|Snippet Change):\s*(.*)$",
            stripped,
            flags=re.IGNORECASE,
        )
        if callout_match:
            flush_paragraph()
            flush_table()
            label = callout_match.group(1).strip()
            message = callout_match.group(2).strip()
            style_map = {
                "lightbulb takeaway": "takeaway_box",
                "definition": "definition_box",
                "note": "note_box",
                "snippet purpose": "snippet_box",
                "snippet change": "note_box",
            }
            style_key = style_map[label.lower()]
            icon = callout_icon(label)
            text = inline_markup(f"{icon}  {label}: {message}" if message else f"{icon}  {label}")
            story.append(KeepTogether([Paragraph(text, styles[style_key])]))
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            flush_table()
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue

        if stripped == "[[AUTO_KEYWORD_INDEX]]":
            flush_paragraph()
            flush_table()
            append_keyword_index()
            continue

        if in_code:
            code.append(line)
            continue

        if "|" in stripped and stripped.startswith("|"):
            flush_paragraph()
            table.append(stripped)
            continue
        flush_table()

        if stripped.startswith("# "):
            flush_paragraph()
            append_recap_extensions()
            heading_text = stripped[2:]
            if not first_heading:
                story.append(PageBreak())
            first_heading = False
            current_chapter_title = chapter_toc_title(heading_text)
            chapter_accent = chapter_accent_for_heading(heading_text)
            has_custom_reflection = False
            has_custom_try_next = False
            para = Paragraph(inline_markup(heading_text), styles["chapter"])
            para._toc_level = 0  # type: ignore[attr-defined]
            para._toc_text = chapter_toc_title(heading_text)  # type: ignore[attr-defined]
            para._running_chapter = chapter_toc_title(heading_text)  # type: ignore[attr-defined]
            para._chapter_accent = chapter_accent  # type: ignore[attr-defined]
            story.append(para)
            append_chapter_band(story, width, chapter_accent)
            continue
        if stripped.startswith("## "):
            flush_paragraph()
            section_text = stripped[3:]
            section_lower = section_text.lower()
            if in_after_learning and section_lower.startswith("reflection questions"):
                has_custom_reflection = True
                in_after_learning = False
            elif in_after_learning and section_lower.startswith("what to try next in this chapter"):
                has_custom_try_next = True
                in_after_learning = False
            else:
                append_recap_extensions()
            if section_text.lower().startswith("after you interact: what you learned"):
                in_after_learning = True
                learned_points = 0
                has_custom_reflection = False
                has_custom_try_next = False
            para = Paragraph(inline_markup(section_text), styles["section"])
            if section_text.lower().startswith(
                ("lightbulb takeaway:", "definition:", "note:", "snippet purpose:", "snippet change:")
            ):
                story.append(para)
                continue
            para._running_section = section_text  # type: ignore[attr-defined]
            story.append(para)
            continue
        if stripped.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped[4:]), styles["section"]))
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            if in_after_learning:
                learned_points += 1
                story.append(Paragraph(inline_markup(stripped[2:]), styles["learned_detail"], bulletText="•"))
            else:
                story.append(Paragraph(inline_markup(stripped[2:]), styles["bullet"], bulletText="•"))
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if numbered:
            flush_paragraph()
            story.append(
                Paragraph(
                    inline_markup(numbered.group(2)),
                    styles["bullet"],
                    bulletText=f"{numbered.group(1)}.",
                )
            )
            continue

        paragraph.append(stripped)

    flush_paragraph()
    append_recap_extensions()
    flush_code()
    flush_table()
    return story


def draw_body_page_background(canvas, doc) -> None:  # type: ignore[no-untyped-def]
    canvas.saveState()
    page_w, page_h = doc.pagesize
    canvas.setFillColor(colors.HexColor("#ececec"))
    canvas.rect(0, 0, page_w, page_h, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#ffffff"))
    canvas.rect(doc.leftMargin - 6 * mm, doc.bottomMargin - 4 * mm, doc.width + 12 * mm, doc.height + 8 * mm, stroke=0, fill=1)
    accent_hex = getattr(doc, "current_chapter_accent", BRAND_ACCENTS[0])
    canvas.setFillColor(tint(accent_hex, 0.84))
    canvas.rect(doc.leftMargin - 6 * mm, doc.bottomMargin - 4 * mm, 1.6 * mm, doc.height + 8 * mm, stroke=0, fill=1)
    canvas.restoreState()


def draw_body_page_overlay(canvas, doc) -> None:  # type: ignore[no-untyped-def]
    canvas.saveState()
    page_w, page_h = doc.pagesize
    accent_hex = getattr(doc, "current_chapter_accent", BRAND_ACCENTS[0])
    accent = colors.HexColor(accent_hex)
    canvas.setStrokeColor(tint(accent_hex, 0.72))
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, page_h - 15 * mm, page_w - doc.rightMargin, page_h - 15 * mm)
    chapter = getattr(doc, "current_running_chapter", "Main")

    canvas.setFillColor(colors.HexColor("#0f172a"))
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(doc.leftMargin, page_h - 11.3 * mm, f"{BOOK_TITLE} | {chapter}")

    # Footer with progress line and page index.
    progress_left = doc.leftMargin
    progress_width = page_w - doc.leftMargin - doc.rightMargin
    progress_bottom = 8.8 * mm
    canvas.setFillColor(colors.HexColor("#cbd5e1"))
    canvas.rect(progress_left, progress_bottom, progress_width, 1.2 * mm, stroke=0, fill=1)
    if PAGE_TOTAL_HINT > 0:
        ratio = min(1.0, max(0.0, canvas.getPageNumber() / PAGE_TOTAL_HINT))
        canvas.setFillColor(accent)
        canvas.rect(progress_left, progress_bottom, progress_width * ratio, 1.2 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#334155"))
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(page_w / 2, 6.2 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def draw_front_matter_page(canvas, doc) -> None:  # type: ignore[no-untyped-def]
    canvas.saveState()
    page_w, _ = doc.pagesize
    canvas.setFillColor(colors.HexColor("#475569"))
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(page_w / 2, 9 * mm, f"{canvas.getPageNumber()}")
    canvas.restoreState()


def render_book(out_pdf: Path) -> None:
    global PAGE_TOTAL_HINT
    ensure_cover_image(COVER_IMAGE)
    lines = clean_lines(BOOK_MD.read_text(encoding="utf-8"))
    validate_book_structure(lines)
    keyword_terms = extract_keyword_terms(lines)
    styles = build_styles()
    page_w, page_h = A4

    def make_doc() -> BookDocTemplate:
        doc = BookDocTemplate(
            str(out_pdf),
            pagesize=A4,
            leftMargin=23 * mm,
            rightMargin=23 * mm,
            topMargin=22 * mm,
            bottomMargin=20 * mm,
            title=f"{BOOK_TITLE} | Kairo",
            author=BOOK_AUTHOR,
            subject="Beginner guide to Kairo",
            keywords=BOOK_KEYWORDS,
            creator=f"{BOOK_PUBLISHER} Production Pipeline",
        )
        cover_frame = Frame(
            0,
            0,
            page_w,
            page_h,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="cover",
        )
        front_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="front")
        body_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
        doc.addPageTemplates(
            [
                PageTemplate(id="cover", frames=[cover_frame]),
                PageTemplate(id="front", frames=[front_frame], onPage=draw_front_matter_page),
                PageTemplate(
                    id="body",
                    frames=[body_frame],
                    onPage=draw_body_page_background,
                    onPageEnd=draw_body_page_overlay,
                ),
            ]
        )
        doc.current_running_chapter = "Preface"
        doc.current_running_section = ""
        doc.current_chapter_accent = BRAND_ACCENTS[0]
        return doc

    body_width = make_doc().width

    def build_story(keyword_map: dict[str, list[int]] | None = None) -> list[object]:
        story: list[object] = []
        story.append(Image(str(COVER_IMAGE), width=page_w, height=page_h))
        story.append(NextPageTemplate("front"))
        story.append(PageBreak())

        story.append(Spacer(1, 18 * mm))
        story.append(Paragraph(BOOK_TITLE, styles["book_title"]))
        story.append(Paragraph("Kairo", styles["book_title"]))
        story.append(Paragraph(BOOK_TAGLINE, styles["book_tag"]))
        story.append(Paragraph(BOOK_SUBTITLE, styles["book_subtitle"]))
        story.append(Spacer(1, 12 * mm))
        story.append(Paragraph(BOOK_AUTHOR, styles["book_meta"]))
        story.append(Paragraph(BOOK_EDITION, styles["book_meta"]))
        story.append(PageBreak())

        story.append(Spacer(1, 90 * mm))
        story.append(
            Paragraph(
                "Dedicated to all of the budding techies of the future.<br/>"
                "The world is ready for your brilliance.",
                styles["dedication"],
            )
        )
        story.append(PageBreak())

        story.append(Paragraph("Copyright", styles["toc_title"]))
        story.append(
            Paragraph(
                "Copyright © 2026 Tech I Can. All rights reserved. "
                "No part of this publication may be reproduced or transmitted "
                "without written permission from the publisher, except for brief quotations "
                "used in educational review.",
                styles["copyright"],
            )
        )
        story.append(
            Paragraph(
                "Published by Tech I Can, for practical AI literacy in schools and workshops. "
                "This classroom edition is designed for guided learning with reproducible exercises.",
                styles["copyright"],
            )
        )
        story.append(Spacer(1, 4 * mm))
        story.append(Paragraph("Publication Data", styles["section"]))
        story.append(Paragraph(f"Publisher: {BOOK_PUBLISHER}", styles["imprint"]))
        story.append(Paragraph(f"Publication date: {BOOK_PUBLICATION_DATE}", styles["imprint"]))
        story.append(Paragraph(BOOK_ISBN, styles["imprint"]))
        story.append(Paragraph(f"Edition: {BOOK_EDITION}", styles["imprint"]))
        story.append(Paragraph("Trim size: A4 digital classroom edition", styles["imprint"]))
        story.append(Spacer(1, 10 * mm))
        story.append(Paragraph(BOOK_TITLE, styles["book_subtitle"]))
        story.append(Paragraph("Curious today, Confident tomorrow.", styles["book_subtitle"]))
        story.append(Spacer(1, 18 * mm))
        story.append(Paragraph("Printed in digital format for classroom distribution.", styles["copyright"]))
        story.append(PageBreak())

        story.append(Paragraph("Contents", styles["toc_title"]))
        toc = TableOfContents()
        toc.levelStyles = [styles["toc_level_0"], styles["toc_level_1"]]
        story.append(toc)
        story.append(NextPageTemplate("body"))
        story.append(PageBreak())

        story.extend(build_body_story(lines, styles, body_width, keyword_page_map=keyword_map))
        return story

    # Pass 1: render manuscript and gather keyword page map.
    make_doc().multiBuild(build_story(), canvasmaker=DeterministicCanvas)
    PAGE_TOTAL_HINT = len(PdfReader(str(out_pdf)).pages)
    keyword_page_map = build_keyword_page_map(out_pdf, keyword_terms)

    # Pass 2: render final book with populated keyword index.
    make_doc().multiBuild(build_story(keyword_map=keyword_page_map), canvasmaker=DeterministicCanvas)
    PAGE_TOTAL_HINT = len(PdfReader(str(out_pdf)).pages)
    apply_accessibility_catalog_tags(out_pdf)
    optimise_pdf_with_ghostscript(out_pdf)


def main() -> int:
    PRINTABLE.mkdir(parents=True, exist_ok=True)
    render_book(BOOK_PDF)
    print(f"Generated {BOOK_PDF.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
