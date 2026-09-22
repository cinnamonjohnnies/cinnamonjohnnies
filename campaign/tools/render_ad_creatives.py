# Renders the 6 LinkedIn ad creative images (1200x627, LinkedIn's single-image
# ad spec) referenced in campaign/02-linkedin-ads.md, then a full ad-card
# mockup for each of the 8 ad variants (2 variants share a creative where the
# copy says so) showing exactly how the ad will render in-feed.
#
# Requires: pip install playwright pillow. Chromium binary via CHROME_PATH env
# var or the fallback path below.
#
# Usage: python3 campaign/tools/render_ad_creatives.py

import os
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAMPAIGN = os.path.join(ROOT, "campaign")
CREATIVE_DIR = os.path.join(CAMPAIGN, "assets", "ad-creatives")
MOCKUP_DIR = os.path.join(CAMPAIGN, "assets", "ad-mockups")
CHROME_PATH = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")

NAVY = "#1b2027"
BLUE = "#285d88"
BLUE2 = "#33719f"
GOLD = "#c8963e"
LIGHT = "#cfe4f4"

BASE_CSS = """
html, body { margin:0; padding:0; overflow:hidden; }
.card {
  position: relative;
  background: linear-gradient(120deg, %s 0%%, #23364a 42%%, %s 78%%, %s 100%%);
  font-family: "Helvetica Neue", Arial, sans-serif;
  box-sizing: border-box;
  width: 1200px; height: 627px;
}
.path { position:absolute; left:0; right:0; top:0; bottom:0; opacity:0.14; }
.brand-row { position:absolute; top:36px; left:44px; display:flex; align-items:center; gap:12px; z-index:2; }
.logo-mark { width:36px; height:36px; filter: invert(1) brightness(2.1); }
.wordmark { line-height:1.05; }
.wordmark .light { display:block; color:#fff; font-weight:300; font-size:16px; letter-spacing:0.02em; }
.wordmark .bold { display:block; color:#fff; font-weight:800; font-size:14px; letter-spacing:0.16em; }
.content { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; z-index:2; }
.rule { width:70px; height:4px; background:%s; border-radius:2px; }
""" % (NAVY, BLUE, BLUE2, GOLD)

PATH_SVG = """
<svg class="path" viewBox="0 0 1200 627" xmlns="http://www.w3.org/2000/svg">
  <path d="M 40 560 C 240 560, 240 380, 440 380 S 640 500, 840 500 S 1080 300, 1150 220"
        fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="1 18" stroke-linecap="round"/>
  <circle cx="40" cy="560" r="9" fill="#ffffff"/>
  <circle cx="440" cy="380" r="9" fill="#ffffff"/>
  <circle cx="840" cy="500" r="9" fill="#ffffff"/>
  <circle cx="1150" cy="220" r="11" fill="%s"/>
</svg>
""" % GOLD

BRAND_ROW = """
<div class="brand-row">
  <img class="logo-mark" src="checkpoint-logo-mark.png" />
  <div class="wordmark"><span class="light">CHECKPOINT</span><span class="bold">PLANNING</span></div>
</div>
"""

def wrap(inner_css, inner_html):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8" />
<style>{BASE_CSS}{inner_css}</style></head>
<body><div class="card">{PATH_SVG}{BRAND_ROW}<div class="content">{inner_html}</div></div></body></html>"""

# ---------------------------------------------------------------------------
# Motif builders
# ---------------------------------------------------------------------------

def quote_motif(line1, line2, subline):
    css = """
    .quote { color:#fff; font-size:46px; font-weight:700; text-align:center; max-width:820px; line-height:1.28; margin:0 0 22px 0; }
    .subline { color:%s; font-size:20px; text-align:center; max-width:640px; line-height:1.5; margin-top:22px; }
    """ % LIGHT
    html = f'<p class="quote">&ldquo;{line1}<br/>{line2}&rdquo;</p><div class="rule"></div><p class="subline">{subline}</p>'
    return css, html

def document_motif(title1, title2, subline):
    css = """
    .doc { width:260px; height:340px; background:#f5f7f9; border-radius:6px; box-shadow:0 18px 40px rgba(0,0,0,0.35);
           display:flex; flex-direction:column; align-items:center; justify-content:center; padding:24px; box-sizing:border-box; margin-bottom:0; }
    .doc .bar { width:60px; height:5px; background:%s; border-radius:3px; margin-bottom:18px; }
    .doc .t1 { color:%s; font-size:13px; font-weight:700; letter-spacing:0.12em; text-align:center; }
    .doc .t2 { color:%s; font-size:22px; font-weight:800; text-align:center; line-height:1.25; margin-top:8px; }
    .doc .t3 { color:#57626c; font-size:12px; text-align:center; margin-top:14px; }
    .subline { color:%s; font-size:20px; text-align:center; max-width:560px; line-height:1.5; margin-top:26px; }
    .row { display:flex; align-items:center; gap:60px; }
    """ % (GOLD, BLUE2, NAVY, LIGHT)
    html = f"""<div class="row">
      <div class="doc"><div class="bar"></div><div class="t1">CHECKPOINT PLANNING</div>
        <div class="t2">{title1}<br/>{title2}</div><div class="t3">A free planning workbook</div></div>
      <div style="max-width:420px;"><p class="subline" style="margin-top:0; text-align:left;">{subline}</p></div>
    </div>"""
    return css, html

def roadmap_motif(headline, subline):
    css = """
    .headline { color:#fff; font-size:34px; font-weight:700; text-align:center; max-width:760px; margin:0 0 46px 0; }
    .markers { display:flex; align-items:center; gap:0; margin-bottom:26px; }
    .marker { display:flex; flex-direction:column; align-items:center; }
    .dot { width:20px; height:20px; border-radius:50%%; background:%s; border:4px solid #fff; }
    .lbl { color:#fff; font-size:16px; font-weight:700; margin-top:10px; }
    .seg { width:130px; height:3px; background:#ffffff; opacity:0.5; margin:0 8px; }
    .subline { color:%s; font-size:20px; text-align:center; max-width:640px; line-height:1.5; }
    """ % (GOLD, LIGHT)
    html = f"""<p class="headline">{headline}</p>
    <div class="markers">
      <div class="marker"><div class="dot"></div><div class="lbl">30 DAYS</div></div>
      <div class="seg"></div>
      <div class="marker"><div class="dot"></div><div class="lbl">90 DAYS</div></div>
      <div class="seg"></div>
      <div class="marker"><div class="dot" style="background:{GOLD};width:26px;height:26px;"></div><div class="lbl">180 DAYS</div></div>
    </div>
    <p class="subline">{subline}</p>"""
    return css, html

def stat_motif(big1, big2, headline, subline):
    css = """
    .statrow { display:flex; align-items:center; gap:36px; margin-bottom:26px; }
    .stat { color:#fff; font-size:96px; font-weight:800; line-height:1; }
    .vs { color:%s; font-size:26px; font-weight:700; }
    .arrow { color:%s; font-size:40px; }
    .headline { color:#fff; font-size:30px; font-weight:700; text-align:center; max-width:760px; margin:0 0 18px 0; }
    .subline { color:%s; font-size:19px; text-align:center; max-width:640px; line-height:1.5; }
    """ % (LIGHT, GOLD, LIGHT)
    html = f"""<div class="statrow"><span class="stat">{big1}</span><span class="arrow">&rarr;</span><span class="stat" style="color:{GOLD};">{big2}</span></div>
    <p class="headline">{headline}</p><div class="rule" style="margin-bottom:16px;"></div><p class="subline">{subline}</p>"""
    return css, html

def checklist_motif(headline, items, subline):
    css = """
    .headline { color:#fff; font-size:30px; font-weight:700; text-align:center; max-width:760px; margin:0 0 26px 0; }
    .list { background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.25); border-radius:10px;
            padding:22px 34px; margin-bottom:24px; }
    .item { display:flex; align-items:center; gap:14px; color:#fff; font-size:19px; font-weight:600; padding:7px 0; }
    .check { width:22px; height:22px; border-radius:5px; background:%s; flex-shrink:0; position:relative; }
    .check::after { content:''; position:absolute; left:6px; top:2px; width:6px; height:11px; border:solid #1b2027; border-width:0 3px 3px 0; transform:rotate(40deg); }
    .subline { color:%s; font-size:19px; text-align:center; max-width:620px; line-height:1.5; }
    """ % (GOLD, LIGHT)
    items_html = "".join(f'<div class="item"><span class="check"></span>{i}</div>' for i in items)
    html = f'<p class="headline">{headline}</p><div class="list">{items_html}</div><p class="subline">{subline}</p>'
    return css, html

CREATIVES = {
    "job-loss-a1-quote": quote_motif("One checkpoint", "at a time.",
        "A free 90-day workbook for the first month after a layoff."),
    "job-loss-a2-workbook": document_motif("YOUR NEXT", "CHECKPOINT",
        "A free 90-day workbook: severance, COBRA, and your old 401(k), in order."),
    "early-retirement-a1-roadmap": roadmap_motif("Retiring Early? Make Sure Your Money Can Too.",
        "The free Early Retirement Checkpoint Guide, built around your actual timeline."),
    "early-retirement-a2-stat": stat_motif("62", "70", "It's Not Just About the Number.",
        "Claiming Social Security early can permanently cut your benefit 25 to 30 percent."),
    "divorce-a1-checklist": checklist_motif("Know the Real Value Before You Sign",
        ["Settlement tax treatment", "Retirement account splits", "Post-divorce cash flow"],
        "A free Divorce Financial Checkpoint Guide. Confidential."),
    "inheritance-a1-quote": quote_motif("Slow down before", "you decide anything.",
        "A free guide to inherited IRAs, cost basis, and what to confirm first."),
}

def render(name, css, html, out_path):
    full_html = wrap(css, html)
    tmp_html = os.path.join(CREATIVE_DIR, f"_{name}.html")
    with open(tmp_html, "w") as f:
        f.write(full_html)
    raw_path = os.path.join(CREATIVE_DIR, f"_{name}_raw.png")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH if os.path.exists(CHROME_PATH) else None)
        page = browser.new_page(viewport={"width": 1200, "height": 627}, device_scale_factor=2)
        page.goto(f"file://{tmp_html}")
        page.wait_for_timeout(120)
        page.screenshot(path=raw_path)
        browser.close()
    img = Image.open(raw_path).resize((1200, 627), Image.LANCZOS)
    img.save(out_path)
    os.remove(tmp_html)
    os.remove(raw_path)
    print("wrote", out_path)

if __name__ == "__main__":
    for name, (css, html) in CREATIVES.items():
        render(name, css, html, os.path.join(CREATIVE_DIR, f"{name}.png"))
