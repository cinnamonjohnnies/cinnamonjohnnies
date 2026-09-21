import os, re, threading, http.server, socketserver, time, functools
from pypdf import PdfWriter, PdfReader
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER

# Regenerates compliance/Checkpoint-Planning-Compliance-Review-Package.pdf from the
# current website/, lead-magnets/, and email-nurture/ content. Requires: pip install
# playwright pillow pypdf reportlab pymupdf, plus a Chromium binary Playwright can find
# (set PLAYWRIGHT_BROWSERS_PATH, or edit the executable_path below).
#
# Usage: python3 compliance/tools/build_compliance_deck.py

# Email nurture sequences are being sent manually for now (automation comes later),
# so they're left out of the compliance package until that's built. Flip this back to
# True once the sequences are ready to submit alongside everything else.
INCLUDE_EMAILS = False

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEB = os.path.join(ROOT, "website")
OUT_DIR = os.path.join(ROOT, "compliance", "_build")
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = colors.HexColor("#1b2027")
BLUE = colors.HexColor("#33719f")
BLUE_DARK = colors.HexColor("#285d88")
GRAY = colors.HexColor("#57626c")
LIGHT = colors.HexColor("#e7eff6")
GOLD = colors.HexColor("#c8963e")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CPTitle", fontName="Helvetica-Bold", fontSize=26, leading=32, textColor=NAVY, spaceAfter=10))
styles.add(ParagraphStyle(name="CPSubtitle", fontName="Helvetica", fontSize=13, leading=18, textColor=GRAY, spaceAfter=6))
styles.add(ParagraphStyle(name="CPSectionDivider", fontName="Helvetica-Bold", fontSize=28, leading=34, textColor=colors.white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="CPSectionSub", fontName="Helvetica", fontSize=12, leading=17, textColor=colors.white, alignment=TA_CENTER, spaceBefore=10))
styles.add(ParagraphStyle(name="CPH1", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=NAVY, spaceBefore=14, spaceAfter=8))
styles.add(ParagraphStyle(name="CPH2", fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=BLUE_DARK, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="CPBody", fontName="Helvetica", fontSize=10, leading=14.5, textColor=colors.HexColor("#232a30"), spaceAfter=7))
styles.add(ParagraphStyle(name="CPBullet", fontName="Helvetica", fontSize=10, leading=14.5, textColor=colors.HexColor("#232a30"), leftIndent=14, spaceAfter=4, bulletIndent=2))
styles.add(ParagraphStyle(name="CPItalic", fontName="Helvetica-Oblique", fontSize=10.5, leading=15, textColor=BLUE_DARK, spaceAfter=8, leftIndent=10, borderColor=BLUE, borderWidth=0, backColor=LIGHT))
styles.add(ParagraphStyle(name="CPMeta", fontName="Helvetica", fontSize=9.5, leading=13, textColor=GRAY))
styles.add(ParagraphStyle(name="CPFooterNote", fontName="Helvetica-Oblique", fontSize=8, leading=11, textColor=GRAY))

def md_inline(text):
    text = text.replace("&", "&amp;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"™", "&trade;", text)
    return text

def markdown_flowables(md_text, h1_style="CPH1", h2_style="CPH2"):
    flow = []
    lines = md_text.split("\n")
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
                    ("BACKGROUND", (0,0), (-1,0), BLUE_DARK),
                    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
                    ("FONTSIZE", (0,0), (-1,-1), 8.5),
                    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dde3e9")),
                    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f7f9")]),
                    ("VALIGN", (0,0), (-1,-1), "TOP"),
                    ("LEFTPADDING", (0,0), (-1,-1), 5),
                    ("RIGHTPADDING", (0,0), (-1,-1), 5),
                    ("TOPPADDING", (0,0), (-1,-1), 4),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
                ]))
                flow.append(t)
                flow.append(Spacer(1, 8))
            table_buf = []

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
        if line.startswith("# "):
            flow.append(Paragraph(md_inline(line[2:]), styles[h1_style]))
        elif line.startswith("## "):
            flow.append(Paragraph(md_inline(line[3:]), styles[h2_style]))
        elif line.startswith("### "):
            flow.append(Paragraph(md_inline(line[4:]), styles["CPH2"]))
        elif line.strip() == "---":
            flow.append(Spacer(1, 4))
            flow.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#dde3e9")))
            flow.append(Spacer(1, 6))
        elif line.strip().startswith("- "):
            flow.append(Paragraph("&bull;&nbsp;&nbsp;" + md_inline(line.strip()[2:]), styles["CPBullet"]))
        elif line.strip().startswith("*") and line.strip().endswith("*") and not line.strip().startswith("**"):
            flow.append(Paragraph(md_inline(line.strip()), styles["CPItalic"]))
        else:
            flow.append(Paragraph(md_inline(line.strip()), styles["CPBody"]))
        i += 1
    flush_table()
    return flow

def section_divider_pdf(path, title, subtitle, badge):
    doc = SimpleDocTemplate(path, pagesize=LETTER, topMargin=0, bottomMargin=0, leftMargin=0, rightMargin=0)
    from reportlab.platypus import Frame, BaseDocTemplate, PageTemplate
    from reportlab.pdfgen import canvas as canvas_mod

    def draw(c, d):
        c.setFillColor(NAVY)
        c.rect(0, 0, LETTER[0], LETTER[1], fill=1, stroke=0)
        c.setFillColor(BLUE_DARK)
        c.rect(0, LETTER[1]/2 - 90, LETTER[0], 180, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(LETTER[0]/2, LETTER[1]/2 + 40, badge.upper())
        c.setFont("Helvetica-Bold", 30)
        c.drawCentredString(LETTER[0]/2, LETTER[1]/2, title)
        c.setFont("Helvetica", 12)
        c.drawCentredString(LETTER[0]/2, LETTER[1]/2 - 30, subtitle)

    c = canvas_mod.Canvas(path, pagesize=LETTER)
    draw(c, None)
    c.showPage()
    c.save()

def build_supplement(path, sections):
    doc = SimpleDocTemplate(path, pagesize=LETTER, topMargin=0.85*inch, bottomMargin=0.75*inch, leftMargin=0.8*inch, rightMargin=0.8*inch)
    story = []
    for kind, payload in sections:
        if kind == "flowables":
            story.extend(payload)
        elif kind == "pagebreak":
            story.append(PageBreak())
    doc.build(story)

# ---------------------------------------------------------------
# 1. Cover page
# ---------------------------------------------------------------
cover_path = os.path.join(OUT_DIR, "00_cover.pdf")
from reportlab.pdfgen import canvas as canvas_mod2

c = canvas_mod2.Canvas(cover_path, pagesize=LETTER)
W, H = LETTER
c.setFillColor(NAVY)
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(BLUE_DARK)
c.rect(0, H-2.6*inch, W, 2.6*inch, fill=1, stroke=0)
c.setFillColor(colors.white)
c.setFont("Helvetica-Bold", 13)
c.drawString(0.9*inch, H-1.0*inch, "CHECKPOINT PLANNING")
c.setFont("Helvetica", 10)
c.drawString(0.9*inch, H-1.25*inch, "Marketing Material Submission for Compliance Review")

c.setFont("Helvetica-Bold", 30)
c.drawString(0.9*inch, H-3.6*inch, "New Marketing Material")
c.setFont("Helvetica-Bold", 30)
c.drawString(0.9*inch, H-4.15*inch, "Compliance Review Package")

c.setFillColor(colors.HexColor("#9cc4e2"))
c.setFont("Helvetica", 13)
_subtitle = "Website (10 pages) and 3 new lead magnets"
if INCLUDE_EMAILS:
    _subtitle += ", and 4 email nurture sequences"
c.drawString(0.9*inch, H-4.7*inch, _subtitle)

c.setFillColor(colors.white)
c.setFont("Helvetica-Bold", 10)
c.drawString(0.9*inch, 1.6*inch, "SUBMITTED BY")
c.setFont("Helvetica", 11)
c.drawString(0.9*inch, 1.38*inch, "Scott Marcoe, CRPC™  —  Founder & Financial Planner, Checkpoint Planning")
c.setFont("Helvetica", 9.5)
c.setFillColor(colors.HexColor("#9cc4e2"))
c.drawString(0.9*inch, 1.18*inch, "Checkpoint Planning — Capstone Financial Group | Ameritas Investment Company, LLC (AIC), Member FINRA/SIPC")
c.drawString(0.9*inch, 1.02*inch, "Ameritas Advisory Services, LLC (AAS)  |  scott@checkpointplanning.com  |  (949) 702-0139")

import datetime
c.setFont("Helvetica", 9.5)
c.setFillColor(colors.white)
c.drawRightString(W-0.9*inch, 1.6*inch, "Date: " + datetime.date.today().strftime("%B %d, %Y"))
c.showPage()
c.save()

# ---------------------------------------------------------------
# 2. Summary / index page
# ---------------------------------------------------------------
summary_flow = []
summary_flow.append(Paragraph("What's in This Package", styles["CPTitle"]))
summary_flow.append(Paragraph(
    "This package contains every piece of new marketing material for the Checkpoint Planning lead-generation "
    "expansion, submitted together for a single compliance review pass.", styles["CPSubtitle"]))
summary_flow.append(Spacer(1, 10))

summary_items = [
    ("1. Website — 10 pages", "Home, About, Services, Our Process, Fees, and Contact (the general site), plus four dedicated landing pages for Job Loss & Layoff, Early Retirement, Divorce, and Inheritance & Unexpected Wealth. Each page below is captured exactly as it renders live, including the footer disclosures and Form CRS links."),
    ("2. Lead magnets — 4 guides", "“Your Next Checkpoint” workbook (existing, previously produced) plus three new companion guides: Early Retirement, Divorce, and Inheritance — offered as opt-in downloads from the matching landing page."),
]
if INCLUDE_EMAILS:
    summary_items.append(
        ("3. Email nurture sequences — 4 sequences, 20 emails total", "A five-email sequence for each transition (job loss, early retirement, divorce, inheritance), sent automatically after a lead magnet download, ending in an invitation to a complimentary Where We Begin session."))
summary_items.append(
    (f"{len(summary_items)+1}. Compliance notes", "A summary of the required disclosures included throughout (fiduciary/FINRA-SIPC language, Form CRS links for AIC and AAS, fee transparency language, “not investment advice” disclaimers) for quick reference during review."))
for h, body in summary_items:
    summary_flow.append(Paragraph(h, styles["CPH2"]))
    summary_flow.append(Paragraph(body, styles["CPBody"]))
    summary_flow.append(Spacer(1, 4))

summary_flow.append(Spacer(1, 10))
summary_flow.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#dde3e9")))
summary_flow.append(Spacer(1, 8))
summary_flow.append(Paragraph("Planned Distribution", styles["CPH2"]))
_distribution_text = (
    "The website is planned to launch at a new subdomain (start.checkpointplanning.com) first, with checkpointplanning.com "
    "itself unchanged until this material is approved. Lead magnets are offered as gated downloads on their matching landing "
    "page"
)
if INCLUDE_EMAILS:
    _distribution_text += "; email sequences are triggered automatically after a download via the firm's email platform"
else:
    _distribution_text += (
        "; follow-up after a download is being handled manually by Scott for now, with the drafted email sequences "
        "held for a future automation build (not included in this submission)"
    )
_distribution_text += ". No paid advertising is planned until this package is approved."
summary_flow.append(Paragraph(_distribution_text, styles["CPBody"]))

build_supplement(os.path.join(OUT_DIR, "01_summary.pdf"), [("flowables", summary_flow)])

print("Cover + summary built")

# ---------------------------------------------------------------
# 3. Section divider pages
# ---------------------------------------------------------------
section_divider_pdf(os.path.join(OUT_DIR, "02_divider_website.pdf"),
    "Section 1", "Website — 10 Pages (Live Render)", "Checkpoint Planning")
section_divider_pdf(os.path.join(OUT_DIR, "04_divider_magnets.pdf"),
    "Section 2", "Lead Magnets — 4 Guides", "Checkpoint Planning")
_next_section = 3
if INCLUDE_EMAILS:
    section_divider_pdf(os.path.join(OUT_DIR, "06_divider_emails.pdf"),
        f"Section {_next_section}", "Email Nurture Sequences — 4 Sequences", "Checkpoint Planning")
    _next_section += 1
section_divider_pdf(os.path.join(OUT_DIR, "08_divider_compliance.pdf"),
    f"Section {_next_section}", "Compliance Notes", "Checkpoint Planning")
print("Dividers built")

# ---------------------------------------------------------------
# 4. Website pages -> PDF via headless Chromium (Playwright)
# ---------------------------------------------------------------
PORT = 8946
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WEB)
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
time.sleep(0.5)

pages = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("process.html", "Our Process"),
    ("fees.html", "Fees"),
    ("contact.html", "Contact"),
    ("job-loss.html", "Job Loss & Layoff Landing Page"),
    ("early-retirement.html", "Early Retirement Landing Page"),
    ("divorce.html", "Divorce Landing Page"),
    ("inheritance.html", "Inheritance & Unexpected Wealth Landing Page"),
]

from playwright.sync_api import sync_playwright
from PIL import Image as PILImage
from reportlab.platypus import Image as RLImage

VIEWPORT_W = 1100  # kept above the 860px mobile breakpoint so screenshots show the desktop layout
PAGE_W_PT, PAGE_H_PT = LETTER
MARGIN_PT = 34
CONTENT_W_PT = PAGE_W_PT - 2 * MARGIN_PT
CONTENT_H_PT = PAGE_H_PT - 2 * MARGIN_PT - 22  # leave room for the label line
SCALE_PT_PER_PX = CONTENT_W_PT / VIEWPORT_W
CHUNK_H_PX = int(CONTENT_H_PT / SCALE_PT_PER_PX)

def screenshot_to_pdf_pages(png_path, out_prefix, label):
    img = PILImage.open(png_path).convert("RGB")
    w, h = img.size
    n_chunks = max(1, -(-h // CHUNK_H_PX))  # ceil
    out_paths = []
    for i in range(n_chunks):
        top = i * CHUNK_H_PX
        bottom = min(h, top + CHUNK_H_PX)
        chunk = img.crop((0, top, w, bottom))
        chunk_path = f"{out_prefix}_{i:02d}.png"
        chunk.save(chunk_path)
        chunk_h_pt = (bottom - top) * SCALE_PT_PER_PX
        page_path = f"{out_prefix}_{i:02d}.pdf"
        c = canvas_mod2.Canvas(page_path, pagesize=LETTER)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 8.5)
        page_note = f"{label}  —  part {i+1} of {n_chunks}" if n_chunks > 1 else label
        c.drawString(MARGIN_PT, PAGE_H_PT - MARGIN_PT + 6, page_note)
        c.drawImage(chunk_path, MARGIN_PT, PAGE_H_PT - MARGIN_PT - 22 - chunk_h_pt,
                    width=CONTENT_W_PT, height=chunk_h_pt)
        c.showPage()
        c.save()
        out_paths.append(page_path)
    return out_paths

website_pdfs = []  # list of lists (one list of page-PDF paths per site page)
with sync_playwright() as p:
    # Adjust this path (or delete the kwarg to use Playwright's own managed browser,
    # after running `playwright install chromium`) to match the Chromium build available
    # in your environment.
    _chrome_path = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    browser = p.chromium.launch(executable_path=_chrome_path) if os.path.exists(_chrome_path) else p.chromium.launch()
    page = browser.new_page(viewport={"width": VIEWPORT_W, "height": 900})
    for idx, (fname, label) in enumerate(pages):
        url = f"http://127.0.0.1:{PORT}/{fname}"
        page.goto(url, wait_until="networkidle")
        png_path = os.path.join(OUT_DIR, f"03_shot_{idx:02d}_{fname.replace('.html','')}.png")
        page.screenshot(path=png_path, full_page=True)
        prefix = os.path.join(OUT_DIR, f"03_page_{idx:02d}_{fname.replace('.html','')}")
        pdf_pages = screenshot_to_pdf_pages(png_path, prefix, f"checkpointplanning.com/{fname}  —  {label}")
        website_pdfs.append(pdf_pages)
        print("Rendered", fname, "->", len(pdf_pages), "page(s)")
    browser.close()

httpd.shutdown()
print("Website pages rendered:", len(website_pdfs))

# ---------------------------------------------------------------
# 5. Lead magnets: existing workbook (as-is) + 3 new guides (from markdown)
# ---------------------------------------------------------------
LEAD_MAGNETS = os.path.join(ROOT, "lead-magnets")

guide_intro_flow = [
    Paragraph("Lead Magnets", styles["CPTitle"]),
    Paragraph(
        "Four downloadable guides, one per transition, offered as the opt-in incentive on the matching "
        "landing page. “Your Next Checkpoint” (job loss) is the firm's existing, previously produced workbook, "
        "included here as-is and reproduced in full on the following pages. The three guides after it "
        "(Early Retirement, Divorce, Inheritance) are new and written to match its structure and tone — "
        "currently in plain-text form, pending final design to match the existing workbook's layout.",
        styles["CPBody"]),
    Spacer(1, 6),
]
build_supplement(os.path.join(OUT_DIR, "05_magnets_intro.pdf"), [("flowables", guide_intro_flow)])

new_guides = [
    ("05b_guide_early_retirement.pdf", os.path.join(LEAD_MAGNETS, "early-retirement-checkpoint-guide.md")),
    ("05c_guide_divorce.pdf", os.path.join(LEAD_MAGNETS, "divorce-financial-checkpoint-guide.md")),
    ("05d_guide_inheritance.pdf", os.path.join(LEAD_MAGNETS, "inheritance-checkpoint-guide.md")),
]
for out_name, md_path in new_guides:
    with open(md_path) as f:
        md_text = f.read()
    flow = markdown_flowables(md_text)
    build_supplement(os.path.join(OUT_DIR, out_name), [("flowables", flow)])
print("Lead magnet guide pages built")

# ---------------------------------------------------------------
# 6. Email nurture sequences (from markdown) — skipped while INCLUDE_EMAILS is False
# ---------------------------------------------------------------
if INCLUDE_EMAILS:
    EMAIL_DIR = os.path.join(ROOT, "email-nurture")
    email_intro_flow = [
        Paragraph("Email Nurture Sequences", styles["CPTitle"]),
        Paragraph(
            "Four five-email sequences (20 emails total), one per transition. Each is triggered automatically when "
            "a visitor downloads the matching lead magnet, spans roughly two weeks, and ends by inviting the reader "
            "to a complimentary Where We Begin session. Merge tags like {{first_name}} are filled in by the email "
            "platform at send time.", styles["CPBody"]),
        Spacer(1, 6),
    ]
    build_supplement(os.path.join(OUT_DIR, "07_emails_intro.pdf"), [("flowables", email_intro_flow)])

    email_files = [
        ("07b_email_job_loss.pdf", os.path.join(EMAIL_DIR, "job-loss-sequence.md")),
        ("07c_email_early_retirement.pdf", os.path.join(EMAIL_DIR, "early-retirement-sequence.md")),
        ("07d_email_divorce.pdf", os.path.join(EMAIL_DIR, "divorce-sequence.md")),
        ("07e_email_inheritance.pdf", os.path.join(EMAIL_DIR, "inheritance-sequence.md")),
    ]
    for out_name, md_path in email_files:
        with open(md_path) as f:
            md_text = f.read()
        flow = markdown_flowables(md_text)
        build_supplement(os.path.join(OUT_DIR, out_name), [("flowables", flow)])
    print("Email sequence pages built")
else:
    print("Skipping email sequence pages (INCLUDE_EMAILS = False)")

# ---------------------------------------------------------------
# 7. Compliance notes / disclosure checklist
# ---------------------------------------------------------------
notes_flow = []
notes_flow.append(Paragraph("Compliance Notes", styles["CPTitle"]))
notes_flow.append(Paragraph(
    "A quick-reference summary of the disclosures and compliance-relevant elements built into this material, "
    "for reviewer convenience. This is not a substitute for full review — it is a map of where things live.",
    styles["CPSubtitle"]))
notes_flow.append(Spacer(1, 8))

_bd_disclosure_scope = "all 10 website pages and all 4 new lead magnets"
if INCLUDE_EMAILS:
    _bd_disclosure_scope += ", and is referenced in email sequence documentation"
checklist = [
    ("Business-name & broker-dealer disclosure",
     f"Present in the footer of {_bd_disclosure_scope}: "
     "“Scott Marcoe offers products and services using the following business names: Checkpoint "
     "Planning — Capstone Financial Group, insurance and financial services | Ameritas Investment Company, LLC "
     "(AIC), Member FINRA/SIPC, securities and investments | Ameritas Advisory Services, LLC (AAS), investment "
     "advisory services. AIC and AAS are not affiliated with Capstone Financial Group.”"),
    ("Form CRS links",
     "Added to the main navigation (a “Form CRS” menu) and the footer of every website page, linking directly to "
     "the AIC Form CRS (ameritas.com/OCM/GetFile?doc=567904) and AAS Form CRS (ameritas.com/OCM/GetFile?doc=567905)."),
    ("“Not investment advice” / educational-purposes language",
     "Present in the footer of all website pages and at the close of all 4 lead magnets."),
    ("Fiduciary standard language",
     "Stated plainly on the Home and Our Process pages (“We are legally required to act in your best interest at "
     "all times—not the firm's interest, not a product manufacturer's, and not our own”) and echoed on each "
     "transition landing page."),
    ("Fee transparency",
     "Full flat-fee planning packages ($1,200 / $2,400 / $4,800) and the tiered AUM fee schedule (0.65%–1.25%) "
     "are published in full on the Fees page, matching the firm's existing Fees & Services document."),
    ("No performance claims or guarantees",
     "No specific investment returns, performance figures, or outcome guarantees appear anywhere in the new "
     "material. All language is process- and service-oriented (the Checkpoint Strategy™ framework, session "
     "structure, and what's included at each fee tier)."),
    ("Testimonials",
     "None are used anywhere in this material."),
    ("Lead capture / data handling",
     "Each form states “Your information is confidential and never sold. No obligation.” Submitted leads are "
     "stored in a private Google Sheet accessible only to Scott Marcoe."),
    ("CRPC™ and licensing credentials",
     "CRPC™ (College for Financial Planning), FINRA/SIPC registration through Ameritas Investment Company, LLC, "
     "and Life & Health license #0E59309 are listed on the About page alongside the CRPC badge graphic."),
]
for h, body in checklist:
    notes_flow.append(Paragraph(h, styles["CPH2"]))
    notes_flow.append(Paragraph(body, styles["CPBody"]))
    notes_flow.append(Spacer(1, 3))

notes_flow.append(Spacer(1, 10))
notes_flow.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#dde3e9")))
notes_flow.append(Spacer(1, 8))
notes_flow.append(Paragraph("Reviewer Sign-Off", styles["CPH2"]))
notes_flow.append(Paragraph(
    "Reviewed by: _______________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date: ______________", styles["CPBody"]))
notes_flow.append(Paragraph(
    "□ Approved as submitted &nbsp;&nbsp;&nbsp; □ Approved with changes (noted below) &nbsp;&nbsp;&nbsp; □ Not approved",
    styles["CPBody"]))
notes_flow.append(Spacer(1, 6))
notes_flow.append(Paragraph("Notes:", styles["CPBody"]))
notes_flow.append(Spacer(1, 60))

build_supplement(os.path.join(OUT_DIR, "09_compliance_notes.pdf"), [("flowables", notes_flow)])
print("Compliance notes page built")

# ---------------------------------------------------------------
# 8. Final merge with bookmarks
# ---------------------------------------------------------------
WORKBOOK_PDF = os.path.join(LEAD_MAGNETS, "your-next-checkpoint-job-loss-workbook.pdf")

writer = PdfWriter()

def add(path, bookmark=None, parent=None, level_kwargs=None):
    reader = PdfReader(path)
    start_page = len(writer.pages)
    for pg in reader.pages:
        writer.add_page(pg)
    if bookmark:
        return writer.add_outline_item(bookmark, start_page, parent=parent)
    return None

add(cover_path)
add(os.path.join(OUT_DIR, "01_summary.pdf"), "Submission Summary")

website_bm = add(os.path.join(OUT_DIR, "02_divider_website.pdf"), "1. Website (10 Pages)")
for (fname, label), pdf_page_paths in zip(pages, website_pdfs):
    first = True
    for pp in pdf_page_paths:
        add(pp, label if first else None, parent=website_bm)
        first = False

magnets_bm = add(os.path.join(OUT_DIR, "04_divider_magnets.pdf"), "2. Lead Magnets (4 Guides)")
add(os.path.join(OUT_DIR, "05_magnets_intro.pdf"), "Overview", parent=magnets_bm)
add(WORKBOOK_PDF, "Your Next Checkpoint (Job Loss) — existing", parent=magnets_bm)
add(os.path.join(OUT_DIR, "05b_guide_early_retirement.pdf"), "Early Retirement Checkpoint Guide — new", parent=magnets_bm)
add(os.path.join(OUT_DIR, "05c_guide_divorce.pdf"), "Divorce Financial Checkpoint Guide — new", parent=magnets_bm)
add(os.path.join(OUT_DIR, "05d_guide_inheritance.pdf"), "Inheritance Checkpoint Guide — new", parent=magnets_bm)

if INCLUDE_EMAILS:
    emails_bm = add(os.path.join(OUT_DIR, "06_divider_emails.pdf"), "3. Email Nurture Sequences")
    add(os.path.join(OUT_DIR, "07_emails_intro.pdf"), "Overview", parent=emails_bm)
    add(os.path.join(OUT_DIR, "07b_email_job_loss.pdf"), "Job Loss & Layoff sequence", parent=emails_bm)
    add(os.path.join(OUT_DIR, "07c_email_early_retirement.pdf"), "Early Retirement sequence", parent=emails_bm)
    add(os.path.join(OUT_DIR, "07d_email_divorce.pdf"), "Divorce sequence", parent=emails_bm)
    add(os.path.join(OUT_DIR, "07e_email_inheritance.pdf"), "Inheritance sequence", parent=emails_bm)

notes_bm = add(os.path.join(OUT_DIR, "08_divider_compliance.pdf"), f"{_next_section}. Compliance Notes")
add(os.path.join(OUT_DIR, "09_compliance_notes.pdf"), "Disclosure checklist & sign-off", parent=notes_bm)

writer.add_metadata({
    "/Title": "Checkpoint Planning - New Marketing Material - Compliance Review Package",
    "/Author": "Scott Marcoe, Checkpoint Planning",
    "/Subject": "Compliance review submission",
})

FINAL_PATH = os.path.join(ROOT, "compliance", "Checkpoint-Planning-Compliance-Review-Package.pdf")
with open(FINAL_PATH, "wb") as f:
    writer.write(f)

print("FINAL PDF built at", FINAL_PATH, "-- total pages:", len(writer.pages))
