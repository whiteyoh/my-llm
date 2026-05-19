from __future__ import annotations

from pathlib import Path
import re
import sys

try:
    import markdown
    from weasyprint import HTML
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "Missing PDF tooling. Install with: pip install markdown weasyprint"
    ) from exc

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PRINTABLE = DOCS / "printable"
ASSETS = DOCS / "assets"
CSS = Path(__file__).with_name("printable.css")

DOC_MAP = {
    "teacher_guide": DOCS / "teacher_guide.md",
    "student_worksheet": DOCS / "student_worksheet.md",
    "first_lesson_walkthrough": DOCS / "first_lesson_walkthrough.md",
}


def with_nav_cues(html: str) -> str:
    parts = re.split(r"(<h2[^>]*>.*?</h2>)", html, flags=re.S)
    if len(parts) < 3:
        return html
    out = []
    h2_titles = [re.sub("<.*?>", "", p).strip() for p in parts if p.startswith("<h2")]
    idx = 0
    for part in parts:
        out.append(part)
        if part.startswith("<h2"):
            prev_title = h2_titles[idx - 1] if idx > 0 else "—"
            next_title = h2_titles[idx + 1] if idx + 1 < len(h2_titles) else "—"
            out.append(f'<div class="nav-cue">Previous: {prev_title} &nbsp;&nbsp;|&nbsp;&nbsp; Next: {next_title}</div>')
            idx += 1
    return "".join(out)


def render(md_path: Path, out_pdf: Path, page_size: str) -> None:
    src = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(src, extensions=["fenced_code", "tables", "toc", "md_in_html"])
    body = body.replace("<pre><code>", '<pre class="command"><code>$ ').replace("</code></pre>", "</code></pre>")
    body = with_nav_cues(body)

    logo_path = ASSETS / "kairo-logo.svg"
    css = CSS.read_text(encoding="utf-8")
    if page_size.lower() == "letter":
        css = css.replace("@page {", "@page letter {")

    html = f"""
    <html><head><meta charset='utf-8'><style>{css}</style></head>
    <body>
      <div class='header'><img src='{logo_path.as_uri()}' alt='Kairo logo'/><span class='title'>Kairo classroom printable</span></div>
      {body}
    </body></html>
    """
    HTML(string=html, base_url=str(DOCS)).write_pdf(str(out_pdf))


def main() -> int:
    page_size = sys.argv[1] if len(sys.argv) > 1 else "A4"
    PRINTABLE.mkdir(parents=True, exist_ok=True)
    for stem, md in DOC_MAP.items():
        render(md, PRINTABLE / f"{stem}.pdf", page_size)
        print(f"Generated {stem}.pdf ({page_size})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
