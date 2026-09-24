import os, re
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfgen import canvas as canvas_mod

# Renders the three lead-magnet guides that only exist as markdown
# (early-retirement, divorce, inheritance) into branded PDFs matching the
# Checkpoint Planning Design System palette, so every landing page's form
# has an actual file to deliver, not just a promise. The fourth guide
# ("Your Next Checkpoint" job-loss workbook) already exists as a designed
# PDF and isn't touched here.
#
# Usage: python3 lead-magnets/tools/build_guide_pdfs.py

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEAD_MAGNETS = os.path.join(ROOT, "lead-magnets")
WEBSITE_LEAD_MAGNETS = os.path.join(ROOT, "website", "lead-magnets")

BLACK = colors.HexColor("#000000")
CHARCOAL = colors.HexColor("#3e3e3e")
TEAL = colors.HexColor("#2e86ab")
INK = colors.HexColor("#1a1b1c")
GRAY = colors.HexColor("#5d5d5d")
LIGHT = colors.HexColor("#f2f2f2")
ON_DARK_MUTED = colors.HexColor("#e3e3e3")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="GTitle", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=INK, spaceBefore=16, spaceAfter=8))
styles.add(ParagraphStyle(name="GH2", fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=TEAL, spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name="GBody", fontName="Helvetica", fontSize=10, leading=14.5, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="GBullet", fontName="Helvetica", fontSize=10, leading=14.5, textColor=INK, leftIndent=14, spaceAfter=4))
styles.add(ParagraphStyle(name="GQuestion", fontName="Helvetica-Oblique", fontSize=10, leading=14.5, textColor=TEAL, spaceAfter=8, leftIndent=10, backColor=LIGHT))
styles.add(ParagraphStyle(name="GFooterNote", fontName="Helvetica-Oblique", fontSize=7.5, leading=11, textColor=GRAY, spaceBefore=12))

def md_inline(text):
    text = text.replace("&", "&amp;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"™", "&trade;", text)
    return text

def markdown_flowables(md_text):
    flow = []
    lines = md_text.strip().split("\n")
    i = 0
    table_buf = []

    def flush_table():
        nonlocal table_buf
        if table_buf:
            rows = [r for r in table_buf if not re.match(r"^\|?\s*-{2,}", r)]
            data = [[c.strip() for c in row.strip().strip("|").split("|")] for row in rows]
            if data:
                t = Table(data, hAlign="LEFT", colWidths=None)
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), CHARCOAL),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d0d0d0")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]))
                flow.append(t)
                flow.append(Spacer(1, 10))
            table_buf = []

    # Skip the first two lines (title/subtitle) and the tagline block, the
    # cover page already carries those.
    while i < len(lines) and not lines[i].startswith("### "):
        i += 1

    while i < len(lines):
        line = lines[i].rstrip()
        if line.strip().startswith("|"):
            table_buf.append(line)
            i += 1
            continue
        else:
            flush_table()

        if not line.strip():
            i += 1
            continue
        if line.startswith("### "):
            flow.append(Paragraph(md_inline(line[4:]), styles["GTitle"]))
        elif line.startswith("**") and line.strip().endswith("**") and not line.strip().startswith("*Question"):
            flow.append(Paragraph(md_inline(line.strip()), styles["GH2"]))
        elif line.strip() == "---":
            flow.append(Spacer(1, 4))
            flow.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#d0d0d0")))
            flow.append(Spacer(1, 8))
        elif line.strip().startswith("- "):
            flow.append(Paragraph("&bull;&nbsp;&nbsp;" + md_inline(line.strip()[2:]), styles["GBullet"]))
        elif line.strip().startswith("*Question to answer:"):
            flow.append(Paragraph(md_inline(line.strip().strip("*")), styles["GQuestion"]))
        elif line.strip().startswith("*") and line.strip().endswith("*") and not line.strip().startswith("**"):
            flow.append(Paragraph(md_inline(line.strip()), styles["GFooterNote"]))
        else:
            flow.append(Paragraph(md_inline(line.strip()), styles["GBody"]))
        i += 1
    flush_table()
    return flow

def cover_page(path, kicker, title, tagline):
    c = canvas_mod.Canvas(path, pagesize=LETTER)
    W, H = LETTER
    c.setFillColor(BLACK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, H - 3.3 * inch, W, 0.06 * inch, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.9 * inch, H - 1.0 * inch, "CHECKPOINT PLANNING")
    c.setFillColor(ON_DARK_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(0.9 * inch, H - 1.25 * inch, "Financial Clarity for Life's In-Betweens")

    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.9 * inch, H - 3.05 * inch, kicker.upper())

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 27)
    title_lines = title
    y = H - 3.75 * inch
    for line in title_lines:
        c.drawString(0.9 * inch, y, line)
        y -= 0.5 * inch

    c.setFillColor(ON_DARK_MUTED)
    c.setFont("Helvetica-Oblique", 13)
    c.drawString(0.9 * inch, y - 0.15 * inch, tagline)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.9 * inch, 1.5 * inch, "Scott Marcoe, CRPC™")
    c.setFillColor(ON_DARK_MUTED)
    c.setFont("Helvetica", 9.5)
    c.drawString(0.9 * inch, 1.3 * inch, "Founder & Financial Planner, Checkpoint Planning")
    c.drawString(0.9 * inch, 1.12 * inch, "(949) 702-0139  |  scott@checkpointplanning.com  |  checkpointplanning.com")
    c.showPage()
    c.save()

def build_guide(md_path, out_path, kicker, title_lines, tagline):
    with open(md_path) as f:
        md_text = f.read()

    tmp_dir = os.path.join(LEAD_MAGNETS, "_build")
    os.makedirs(tmp_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(out_path))[0]
    cover_path = os.path.join(tmp_dir, base + "_cover.pdf")
    content_path = os.path.join(tmp_dir, base + "_content.pdf")

    cover_page(cover_path, kicker, title_lines, tagline)

    doc = SimpleDocTemplate(content_path, pagesize=LETTER, topMargin=0.85 * inch,
                             bottomMargin=0.75 * inch, leftMargin=0.85 * inch, rightMargin=0.85 * inch)
    doc.build(markdown_flowables(md_text))

    from pypdf import PdfWriter, PdfReader
    writer = PdfWriter()
    for p in [cover_path, content_path]:
        reader = PdfReader(p)
        for pg in reader.pages:
            writer.add_page(pg)
    writer.add_metadata({
        "/Title": "Checkpoint Planning - " + " ".join(title_lines),
        "/Author": "Scott Marcoe, Checkpoint Planning",
    })
    with open(out_path, "wb") as f:
        writer.write(f)
    print("Built", out_path, "-", len(writer.pages), "pages")

if __name__ == "__main__":
    build_guide(
        os.path.join(LEAD_MAGNETS, "early-retirement-checkpoint-guide.md"),
        os.path.join(LEAD_MAGNETS, "early-retirement-checkpoint-guide.pdf"),
        "Your Next Checkpoint",
        ["The Early Retirement", "Checkpoint Guide"],
        "A simple guide to the decisions that don't wait until 65.",
    )
    build_guide(
        os.path.join(LEAD_MAGNETS, "divorce-financial-checkpoint-guide.md"),
        os.path.join(LEAD_MAGNETS, "divorce-financial-checkpoint-guide.pdf"),
        "Your Next Checkpoint",
        ["The Divorce Financial", "Checkpoint Guide"],
        "A simple guide to the financial questions behind the legal ones.",
    )
    build_guide(
        os.path.join(LEAD_MAGNETS, "inheritance-checkpoint-guide.md"),
        os.path.join(LEAD_MAGNETS, "inheritance-checkpoint-guide.pdf"),
        "Your Next Checkpoint",
        ["The Inheritance", "Checkpoint Guide"],
        "A simple guide for the first 90 days after an inheritance.",
    )

    # Copy all 4 guide PDFs into website/lead-magnets/ so they actually ship
    # with the site (resources.html links to them with a same-site relative
    # path; anything living only at the repo's top-level lead-magnets/ folder
    # never gets uploaded when only website/'s contents are deployed).
    import shutil
    os.makedirs(WEBSITE_LEAD_MAGNETS, exist_ok=True)
    for fname in [
        "your-next-checkpoint-job-loss-workbook.pdf",
        "early-retirement-checkpoint-guide.pdf",
        "divorce-financial-checkpoint-guide.pdf",
        "inheritance-checkpoint-guide.pdf",
    ]:
        shutil.copyfile(os.path.join(LEAD_MAGNETS, fname), os.path.join(WEBSITE_LEAD_MAGNETS, fname))
    print("Copied 4 guide PDFs into website/lead-magnets/ for deployment")
