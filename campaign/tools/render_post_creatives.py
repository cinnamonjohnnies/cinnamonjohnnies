# Renders 12 quote-card images (1200x1200, same design system as
# website/assets/linkedin-post-image-01.png) for the Month 1 content
# calendar, one per post, each using a line pulled verbatim from that
# post's own approved copy in campaign/08-linkedin-content-calendar-month1.md.
#
# Requires: pip install playwright pillow.
# Usage: python3 campaign/tools/render_post_creatives.py

import os
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAMPAIGN = os.path.join(ROOT, "campaign")
OUT_DIR = os.path.join(CAMPAIGN, "assets", "post-creatives")
CHROME_PATH = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")

# (post number, quote line1, quote line2 or "", subline)
QUOTES = [
    (1, "Clarity has to come", "before a plan means anything.", "Phase 1: Where We Begin."),
    (2, "The goal of the first month", "isn't a plan. It's stability.", "Job Loss & Layoff: the first 30 days."),
    (3, "It's not a marketing word here.", "It's a legal standard.", "What “fiduciary” actually means."),
    (4, "Protecting what you have", "comes before growing it.", "Phase 2: Identify and Protect."),
    (5, "Retiring earlier doesn't mean", "claiming earlier.", "Early Retirement: Social Security timing."),
    (6, "Progress happens through", "checkpoints, not one big push.", "What endurance racing taught me."),
    (7, "This is where the", "actual plan gets built.", "Phase 3: Plot Checkpoints."),
    (8, "A settlement's headline number", "isn't its real value.", "Divorce: the after-tax value of a settlement."),
    (9, "You work directly with me.", "Every meeting, every review.", "Why direct access matters."),
    (10, "Five phases, one process,", "the same structure.", "Phase 4 & 5: Implement, Track and Reset."),
    (11, "Almost nothing about an", "inheritance needs to be decided quickly.", "Inheritance: the step-up in cost basis."),
    (12, "One checkpoint", "at a time.", "Month 1 recap."),
]

TEMPLATE = """<!DOCTYPE html><html><head><meta charset="UTF-8" /><style>
  html, body { margin:0; padding:0; width:1200px; height:1200px; overflow:hidden; }
  .card { width:1200px; height:1200px; position:relative;
    background: linear-gradient(160deg, #1b2027 0%%, #23364a 42%%, #285d88 78%%, #33719f 100%%);
    font-family:"Helvetica Neue", Arial, sans-serif; display:flex; flex-direction:column;
    align-items:center; justify-content:center; box-sizing:border-box; }
  .path { position:absolute; inset:0; opacity:0.14; }
  .brand-row { display:flex; align-items:center; gap:18px; margin-bottom:56px; z-index:2; }
  .logo-mark { width:64px; height:64px; filter:invert(1) brightness(2.1); }
  .wordmark { line-height:1.05; }
  .wordmark .light { display:block; color:#fff; font-weight:300; font-size:30px; letter-spacing:0.02em; }
  .wordmark .bold { display:block; color:#fff; font-weight:800; font-size:27px; letter-spacing:0.18em; }
  .quote { z-index:2; color:#fff; font-size:60px; font-weight:700; text-align:center; max-width:940px; line-height:1.25; margin:0 0 28px 0; }
  .rule { width:90px; height:5px; background:#c8963e; border-radius:3px; margin:0 0 28px 0; z-index:2; }
  .subline { z-index:2; color:#cfe4f4; font-size:26px; font-weight:400; text-align:center; max-width:780px; line-height:1.5; }
  .tagline { position:absolute; bottom:64px; left:0; right:0; text-align:center; color:#9cc4e2; font-size:20px; letter-spacing:0.04em; z-index:2; }
</style></head><body>
<div class="card">
  <svg class="path" viewBox="0 0 1200 1200" xmlns="http://www.w3.org/2000/svg">
    <path d="M 60 1120 C 260 1120, 260 820, 460 820 S 660 1020, 860 1020 S 1080 700, 1140 620"
          fill="none" stroke="#ffffff" stroke-width="4" stroke-dasharray="1 20" stroke-linecap="round"/>
    <circle cx="60" cy="1120" r="11" fill="#ffffff"/><circle cx="460" cy="820" r="11" fill="#ffffff"/>
    <circle cx="860" cy="1020" r="11" fill="#ffffff"/><circle cx="1140" cy="620" r="14" fill="#c8963e"/>
  </svg>
  <div class="brand-row">
    <img class="logo-mark" src="../linkedin-banner/checkpoint-logo-mark.png" />
    <div class="wordmark"><span class="light">CHECKPOINT</span><span class="bold">PLANNING</span></div>
  </div>
  <p class="quote">&ldquo;%s<br/>%s&rdquo;</p>
  <div class="rule"></div>
  <p class="subline">%s</p>
  <p class="tagline">FINANCIAL CLARITY FOR LIFE'S IN-BETWEENS</p>
</div></body></html>"""

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render(num, l1, l2, subline):
    html = TEMPLATE % (esc(l1), esc(l2), esc(subline))
    tmp_html = os.path.join(OUT_DIR, f"_post_{num:02d}.html")
    with open(tmp_html, "w") as f:
        f.write(html)
    raw_path = os.path.join(OUT_DIR, f"_post_{num:02d}_raw.png")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH if os.path.exists(CHROME_PATH) else None)
        page = browser.new_page(viewport={"width": 1200, "height": 1200}, device_scale_factor=2)
        page.goto(f"file://{tmp_html}")
        page.wait_for_timeout(120)
        page.screenshot(path=raw_path)
        browser.close()
    img = Image.open(raw_path).resize((1200, 1200), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, f"post-{num:02d}.png")
    img.save(out_path)
    os.remove(tmp_html)
    os.remove(raw_path)
    print("wrote", out_path)

if __name__ == "__main__":
    for num, l1, l2, subline in QUOTES:
        render(num, l1, l2, subline)
