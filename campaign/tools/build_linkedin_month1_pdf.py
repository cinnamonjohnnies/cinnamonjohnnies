# Regenerates compliance/LinkedIn-Month-1-Compliance-Submission.pdf from
# campaign/08-linkedin-content-calendar-month1.md and campaign/02-linkedin-ads.md.
# Requires: pip install pypdf reportlab
#
# Usage: python3 campaign/tools/build_linkedin_month1_pdf.py

import os
import re
import datetime
from pypdf import PdfWriter, PdfReader
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas as canvas_mod

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAMPAIGN = os.path.join(ROOT, "campaign")
OUT_DIR = os.path.join(CAMPAIGN, "_build_month1")
os.makedirs(OUT_DIR, exist_ok=True)
FINAL_PATH = os.path.join(ROOT, "compliance", "LinkedIn-Month-1-Compliance-Submission.pdf")

NAVY = colors.HexColor("#1b2027")
BLUE = colors.HexColor("#33719f")
BLUE_DARK = colors.HexColor("#285d88")
GRAY = colors.HexColor("#57626c")
LIGHT = colors.HexColor("#e7eff6")
GOLD = colors.HexColor("#c8963e")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CPTitle", fontName="Helvetica-Bold", fontSize=26, leading=32, textColor=NAVY, spaceAfter=10))
styles.add(ParagraphStyle(name="CPSubtitle", fontName="Helvetica", fontSize=13, leading=18, textColor=GRAY, spaceAfter=6))
styles.add(ParagraphStyle(name="CPH1", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=NAVY, spaceBefore=14, spaceAfter=8))
styles.add(ParagraphStyle(name="CPH2", fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=BLUE_DARK, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="CPBody", fontName="Helvetica", fontSize=10, leading=14.5, textColor=colors.HexColor("#232a30"), spaceAfter=7))
styles.add(ParagraphStyle(name="CPBullet", fontName="Helvetica", fontSize=10, leading=14.5, textColor=colors.HexColor("#232a30"), leftIndent=14, spaceAfter=4))
styles.add(ParagraphStyle(name="CPDisclosure", fontName="Helvetica-Oblique", fontSize=8.5, leading=12.5, textColor=GRAY, spaceBefore=4, spaceAfter=14, leftIndent=10))
styles.add(ParagraphStyle(name="CPMeta", fontName="Helvetica-Bold", fontSize=9, leading=13, textColor=BLUE_DARK, spaceBefore=2, spaceAfter=2))

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def md_inline(text):
    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = text.replace("™", "&trade;")
    return text

def section_divider_pdf(path, title, subtitle, badge):
    c = canvas_mod.Canvas(path, pagesize=LETTER)
    W, H = LETTER
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BLUE_DARK)
    c.rect(0, H/2 - 90, W, 180, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W/2, H/2 + 40, badge.upper())
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W/2, H/2, title)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W/2, H/2 - 30, subtitle)
    c.showPage()
    c.save()

def build_doc(path, flow):
    doc = SimpleDocTemplate(path, pagesize=LETTER, topMargin=0.85*inch, bottomMargin=0.75*inch, leftMargin=0.8*inch, rightMargin=0.8*inch)
    doc.build(flow)

# ---------------------------------------------------------------
# Parse campaign/08-linkedin-content-calendar-month1.md
# ---------------------------------------------------------------
with open(os.path.join(CAMPAIGN, "08-linkedin-content-calendar-month1.md")) as f:
    cal_text = f.read()

schedule_match = re.search(r"## Posting schedule\n\n(.*?)\n\nReschedule", cal_text, re.S)
schedule_rows = []
if schedule_match:
    for line in schedule_match.group(1).strip().split("\n"):
        if line.startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            schedule_rows.append(cells)

post_blocks = re.findall(r"## Post (\d+), ([^\n]+)\n\n(.*?)(?=\n---\n\n## Post|\Z)", cal_text, re.S)

# ---------------------------------------------------------------
# Parse campaign/02-linkedin-ads.md
# ---------------------------------------------------------------
with open(os.path.join(CAMPAIGN, "02-linkedin-ads.md")) as f:
    ads_text = f.read()

ad_sections = re.findall(r"## ([^\n]+)\n\nDestination: `([^`]+)`\n\n(.*?)(?=\n---\n\n## |\Z)", ads_text, re.S)

def variant_flowables(variant_text):
    flow = []
    lines = [l for l in variant_text.strip().split("\n") if l.strip()]
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("### "):
            flow.append(Paragraph(md_inline(line[4:]), styles["CPMeta"]))
        elif line.startswith("**") and "**" in line[2:]:
            flow.append(Paragraph(md_inline(line), styles["CPBody"]))
        elif line.startswith("*Note:"):
            flow.append(Paragraph(md_inline(line.strip("*")), styles["CPDisclosure"]))
        else:
            flow.append(Paragraph(md_inline(line), styles["CPBody"]))
        i += 1
    return flow

# ---------------------------------------------------------------
# 1. Cover
# ---------------------------------------------------------------
cover_path = os.path.join(OUT_DIR, "00_cover.pdf")
c = canvas_mod.Canvas(cover_path, pagesize=LETTER)
W, H = LETTER
c.setFillColor(NAVY)
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(BLUE_DARK)
c.rect(0, H-2.6*inch, W, 2.6*inch, fill=1, stroke=0)
c.setFillColor(colors.white)
c.setFont("Helvetica-Bold", 13)
c.drawString(0.9*inch, H-1.0*inch, "CHECKPOINT PLANNING")
c.setFont("Helvetica", 10)
c.drawString(0.9*inch, H-1.25*inch, "LinkedIn Marketing Material, Compliance Submission")

c.setFont("Helvetica-Bold", 28)
c.drawString(0.9*inch, H-3.5*inch, "LinkedIn Content and Ads")
c.setFont("Helvetica-Bold", 28)
c.drawString(0.9*inch, H-4.0*inch, "Month 1 Compliance Submission")

c.setFillColor(colors.HexColor("#9cc4e2"))
c.setFont("Helvetica", 13)
c.drawString(0.9*inch, H-4.55*inch, "12 organic posts, posting schedule, and ad copy for all 4 segments")

c.setFillColor(colors.white)
c.setFont("Helvetica-Bold", 10)
c.drawString(0.9*inch, 1.6*inch, "SUBMITTED BY")
c.setFont("Helvetica", 11)
c.drawString(0.9*inch, 1.38*inch, "Scott Marcoe, CRPC (TM), Founder & Financial Planner, Checkpoint Planning")
c.setFont("Helvetica", 9.5)
c.setFillColor(colors.HexColor("#9cc4e2"))
c.drawString(0.9*inch, 1.18*inch, "Checkpoint Planning, Capstone Financial Group | Ameritas Investment Company, LLC (AIC), Member FINRA/SIPC")
c.drawString(0.9*inch, 1.02*inch, "Ameritas Advisory Services, LLC (AAS)  |  scott@checkpointplanning.com  |  (949) 702-0139")

c.setFont("Helvetica", 9.5)
c.setFillColor(colors.white)
c.drawRightString(W-0.9*inch, 1.6*inch, "Date: " + datetime.date.today().strftime("%B %d, %Y"))
c.showPage()
c.save()

# ---------------------------------------------------------------
# 2. Summary
# ---------------------------------------------------------------
summary_flow = [
    Paragraph("What's in This Submission", styles["CPTitle"]),
    Paragraph(
        "This package bundles a month of LinkedIn organic content with the ad copy for all four "
        "transition segments, submitted together so the whole month can run without a mid-month "
        "compliance gap.", styles["CPSubtitle"]),
    Spacer(1, 10),
    Paragraph("1. Organic posts, 12 posts", styles["CPH2"]),
    Paragraph(
        "Three per week for four weeks (Monday/Wednesday/Friday), rotating through transition "
        "education, a five-part Checkpoint Strategy explainer series, personal story, and "
        "fiduciary/practice differentiator content. Each post includes its disclosure line and "
        "hashtags exactly as they'll be published.", styles["CPBody"]),
    Paragraph("2. LinkedIn ad copy, 4 segments, 8 ads", styles["CPH2"]),
    Paragraph(
        "Two variants each for Job Loss & Layoff, Early Retirement, Divorce, and Inheritance. "
        "Job Loss is the only segment launching immediately (Phase 1 of the budget and testing "
        "plan); the other three are included now so a later phase does not require a second "
        "compliance round-trip.", styles["CPBody"]),
    Spacer(1, 10),
    HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#dde3e9")),
    Spacer(1, 8),
    Paragraph("Not included in this submission", styles["CPH2"]),
    Paragraph(
        "Facebook/Instagram ad copy (separate platform, not part of the current push) and email "
        "nurture sequences (follow-up is being handled manually for now).", styles["CPBody"]),
]
build_doc(os.path.join(OUT_DIR, "01_summary.pdf"), summary_flow)

# ---------------------------------------------------------------
# 3. Posting schedule table
# ---------------------------------------------------------------
section_divider_pdf(os.path.join(OUT_DIR, "02_divider_schedule.pdf"), "Section 1", "Posting Schedule", "Checkpoint Planning")

schedule_flow = [Paragraph("Posting Schedule", styles["CPTitle"]), Spacer(1, 10)]
if schedule_rows:
    header, rows = schedule_rows[0], schedule_rows[1:]
    table_data = [header] + rows
    t = Table(table_data, hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BLUE_DARK),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dde3e9")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f7f9")]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    schedule_flow.append(t)
build_doc(os.path.join(OUT_DIR, "03_schedule.pdf"), schedule_flow)

# ---------------------------------------------------------------
# 4. Organic posts
# ---------------------------------------------------------------
section_divider_pdf(os.path.join(OUT_DIR, "04_divider_posts.pdf"), "Section 2", "Organic Posts (12)", "Checkpoint Planning")

post_paths = []
for num, headline, body in post_blocks:
    flow = [Paragraph(f"Post {num}: {md_inline(headline.strip())}", styles["CPH1"])]
    body = body.strip()
    paras = re.split(r"\n\n+", body)
    for para in paras:
        para = para.strip()
        if not para:
            continue
        if para.startswith("**Disclosure:**"):
            flow.append(Paragraph(md_inline(para), styles["CPDisclosure"]))
        elif para.startswith("#"):
            flow.append(Paragraph(md_inline(para), styles["CPMeta"]))
        else:
            para_html = md_inline(para).replace("\n", "<br/>")
            flow.append(Paragraph(para_html, styles["CPBody"]))
    out_path = os.path.join(OUT_DIR, f"05_post_{int(num):02d}.pdf")
    build_doc(out_path, flow)
    post_paths.append((num, headline.strip(), out_path))

# ---------------------------------------------------------------
# 5. Ad copy
# ---------------------------------------------------------------
section_divider_pdf(os.path.join(OUT_DIR, "06_divider_ads.pdf"), "Section 3", "LinkedIn Ad Copy (4 Segments)", "Checkpoint Planning")

ad_paths = []
for title, destination, body in ad_sections:
    flow = [
        Paragraph(md_inline(title.strip()), styles["CPH1"]),
        Paragraph(f"Destination: {esc(destination)}", styles["CPMeta"]),
        Spacer(1, 6),
    ]
    flow.extend(variant_flowables(body))
    out_path = os.path.join(OUT_DIR, f"07_ad_{re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')}.pdf")
    build_doc(out_path, flow)
    ad_paths.append((title.strip(), out_path))

# ---------------------------------------------------------------
# 6. Sign-off
# ---------------------------------------------------------------
signoff_flow = [
    Paragraph("Reviewer Sign-Off", styles["CPTitle"]),
    Paragraph(
        "Reviewed by: _______________________________     Date: ______________", styles["CPBody"]),
    Paragraph(
        "[ ] Approved as submitted    [ ] Approved with changes (noted below)    [ ] Not approved",
        styles["CPBody"]),
    Spacer(1, 6),
    Paragraph("Notes:", styles["CPBody"]),
    Spacer(1, 200),
]
build_doc(os.path.join(OUT_DIR, "08_signoff.pdf"), signoff_flow)

# ---------------------------------------------------------------
# 7. Merge with bookmarks
# ---------------------------------------------------------------
writer = PdfWriter()

def add(path, bookmark=None, parent=None):
    reader = PdfReader(path)
    start = len(writer.pages)
    for pg in reader.pages:
        writer.add_page(pg)
    if bookmark:
        return writer.add_outline_item(bookmark, start, parent=parent)
    return None

add(cover_path)
add(os.path.join(OUT_DIR, "01_summary.pdf"), "Submission Summary")

sched_bm = add(os.path.join(OUT_DIR, "02_divider_schedule.pdf"), "1. Posting Schedule")
add(os.path.join(OUT_DIR, "03_schedule.pdf"), "Calendar", parent=sched_bm)

posts_bm = add(os.path.join(OUT_DIR, "04_divider_posts.pdf"), "2. Organic Posts (12)")
for num, headline, path in post_paths:
    add(path, f"Post {num}: {headline}", parent=posts_bm)

ads_bm = add(os.path.join(OUT_DIR, "06_divider_ads.pdf"), "3. LinkedIn Ad Copy")
for title, path in ad_paths:
    add(path, title, parent=ads_bm)

add(os.path.join(OUT_DIR, "08_signoff.pdf"), "4. Reviewer Sign-Off")

writer.add_metadata({
    "/Title": "Checkpoint Planning - LinkedIn Month 1 - Compliance Submission",
    "/Author": "Scott Marcoe, Checkpoint Planning",
    "/Subject": "Compliance review submission",
})

with open(FINAL_PATH, "wb") as f:
    writer.write(f)

print("FINAL PDF built at", FINAL_PATH, "-- total pages:", len(writer.pages))
print("Posts parsed:", len(post_paths), " Ads parsed:", len(ad_paths))
