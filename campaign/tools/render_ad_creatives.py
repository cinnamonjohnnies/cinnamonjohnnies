# Renders the 6 LinkedIn ad creative images (1200x627, LinkedIn's single-image
# ad spec) referenced in campaign/02-linkedin-ads.md, built from the
# "Checkpoint Planning" Claude Design System: monochrome (black/white/gray)
# with the single teal accent (#2E86AB), Montserrat/Roboto, the real logo,
# and a real photo of Scott (human faces consistently outperform
# abstract/graphic-only ads in LinkedIn benchmarks, see the earlier research
# discussed with the user). Stat/checklist elements that carry real
# information (62 vs 70, the settlement checklist) stay as compact
# supporting detail, not the whole ad.
#
# Requires: pip install playwright pillow. Chromium binary via CHROME_PATH
# env var or the fallback path below.
#
# Usage: python3 campaign/tools/render_ad_creatives.py

import os
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAMPAIGN = os.path.join(ROOT, "campaign")
CREATIVE_DIR = os.path.join(CAMPAIGN, "assets", "ad-creatives")
CHROME_PATH = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
LOGO = "../../../website/assets/checkpoint-logo-white.png"
HEADSHOT = "../../../website/assets/scott-marcoe.jpg"

BLACK = "#000000"
CHARCOAL = "#3e3e3e"
TEAL = "#2e86ab"
ON_DARK = "#ffffff"
ON_DARK_MUTED = "#e3e3e3"
LINK_ON_DARK = "#7cc3df"

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Roboto:wght@400;700&display=swap" rel="stylesheet" />'

BASE_CSS = """
html, body { margin:0; padding:0; overflow:hidden; }
.card { width:1200px; height:627px; position:relative; display:flex;
  font-family:"Roboto", Arial, sans-serif; box-sizing:border-box; background:%s; }
.photo-col { width:460px; height:627px; position:relative; flex-shrink:0; overflow:hidden; }
.photo-col img { width:100%%; height:100%%; object-fit:cover; object-position:center 12%%; }
.photo-col .tint { position:absolute; inset:0; background:linear-gradient(105deg, rgba(0,0,0,0.08) 0%%, rgba(0,0,0,0.4) 100%%); }
.photo-col .edge { position:absolute; top:0; right:-1px; bottom:0; width:60px;
  background:linear-gradient(90deg, rgba(0,0,0,0) 0%%, %s 100%%); }
.content-col { flex:1; position:relative; background:%s;
  padding:44px 52px; box-sizing:border-box; display:flex; flex-direction:column; }
.brand-row { display:flex; align-items:center; gap:10px; z-index:2; margin-bottom:auto; }
.logo-img { height:26px; width:auto; }
.body-wrap { z-index:2; }
.headline { color:%s; font-family:"Montserrat", Arial, sans-serif; font-size:38px; font-weight:800; line-height:1.2; margin:0 0 14px 0; }
.rule { width:60px; height:4px; background:%s; border-radius:2px; margin:0 0 16px 0; }
.subline { color:%s; font-size:19px; line-height:1.45; max-width:600px; margin:0; }
""" % (BLACK, BLACK, CHARCOAL, ON_DARK, TEAL, ON_DARK_MUTED)

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def photo_ad(headline, subline, extra_css="", extra_html=""):
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8" />{FONT_LINK}<style>{BASE_CSS}{extra_css}</style></head>
<body><div class="card">
  <div class="photo-col"><img src="{HEADSHOT}" /><div class="tint"></div><div class="edge"></div></div>
  <div class="content-col">
    <div class="brand-row"><img class="logo-img" src="{LOGO}" /></div>
    <div class="body-wrap"><p class="headline">{headline}</p><div class="rule"></div>
      <p class="subline">{subline}</p>{extra_html}</div>
  </div>
</div></body></html>"""
    return html

def stat_extra(big1, big2):
    css = """
    .statrow { display:flex; align-items:center; gap:16px; margin-top:18px; }
    .stat { color:%s; font-family:"Montserrat", Arial, sans-serif; font-size:44px; font-weight:800; line-height:1; }
    .arrow { color:%s; font-size:20px; }
    """ % (ON_DARK, TEAL)
    html = f'<div class="statrow"><span class="stat">{big1}</span><span class="arrow">&rarr;</span><span class="stat" style="color:{TEAL};">{big2}</span></div>'
    return css, html

def checklist_extra(items):
    css = """
    .clist { margin-top:16px; }
    .citem { display:flex; align-items:center; gap:10px; color:%s; font-size:16px; font-weight:700; padding:4px 0; }
    .cmark { width:16px; height:16px; border-radius:4px; background:%s; flex-shrink:0; }
    """ % (ON_DARK, TEAL)
    items_html = "".join(f'<div class="citem"><span class="cmark"></span>{i}</div>' for i in items)
    html = f'<div class="clist">{items_html}</div>'
    return css, html

CREATIVES = {}

CREATIVES["job-loss-a1-quote"] = (photo_ad(
    "Just Lost Your Job?<br/>Get a Clear 90-Day Plan.",
    "A free workbook built to help you slow down and know what to do first."), )

CREATIVES["job-loss-a2-workbook"] = (photo_ad(
    "A 90-Day Plan for<br/>Your Next Chapter",
    "The free “Your Next Checkpoint” workbook. Fiduciary guidance, not a sales pitch."), )

er_css, er_html = stat_extra("62", "70")
CREATIVES["early-retirement-a1-roadmap"] = (photo_ad(
    "Retiring Early?<br/>Make Sure Your Money Can Too.",
    "Free guide + a complimentary session with a CRPC™ planner.", er_css, er_html), )

er2_css, er2_html = stat_extra("62", "70")
CREATIVES["early-retirement-a2-stat"] = (photo_ad(
    "It's Not Just<br/>About the Number.",
    "Claiming Social Security early can permanently cut your benefit 25 to 30 percent.", er2_css, er2_html), )

div_css, div_html = checklist_extra(["Settlement tax treatment", "Retirement account splits", "Post-divorce cash flow"])
CREATIVES["divorce-a1-checklist"] = (photo_ad(
    "Know the Real Value<br/>Before You Sign",
    "A free Divorce Financial Checkpoint Guide. Confidential.", div_css, div_html), )

CREATIVES["inheritance-a1-quote"] = (photo_ad(
    "Slow Down Before<br/>You Decide Anything.",
    "A free guide to inherited IRAs, cost basis, and what to confirm first."), )

def render(name, html):
    tmp_html = os.path.join(CREATIVE_DIR, f"_{name}.html")
    with open(tmp_html, "w") as f:
        f.write(html)
    raw_path = os.path.join(CREATIVE_DIR, f"_{name}_raw.png")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH if os.path.exists(CHROME_PATH) else None)
        page = browser.new_page(viewport={"width": 1200, "height": 627}, device_scale_factor=2)
        page.goto(f"file://{tmp_html}")
        page.wait_for_timeout(400)
        page.screenshot(path=raw_path)
        browser.close()
    img = Image.open(raw_path).resize((1200, 627), Image.LANCZOS)
    out_path = os.path.join(CREATIVE_DIR, f"{name}.png")
    img.save(out_path)
    os.remove(tmp_html)
    os.remove(raw_path)
    print("wrote", out_path)

if __name__ == "__main__":
    for name, (html,) in CREATIVES.items():
        render(name, html)
