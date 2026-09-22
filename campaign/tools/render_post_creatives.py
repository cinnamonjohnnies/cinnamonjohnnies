# Renders the 12 post images (1200x1200) for the Month 1 content calendar.
# Rotates through 5 on-brand layouts (quote, 5-phase roadmap, checklist,
# stat callout, photo) so a month of posts has visual rhythm instead of one
# template repeated 12 times, while reusing the exact same color system,
# logo, and motif language as the ad creatives in render_ad_creatives.py so
# organic and paid content reinforce each other. All copy lines are pulled
# verbatim (or lightly trimmed) from each post's own approved text in
# campaign/08-linkedin-content-calendar-month1.md.
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
LOGO = "../linkedin-banner/checkpoint-logo-mark.png"
HEADSHOT = "../../../website/assets/scott-marcoe.jpg"

NAVY = "#1b2027"
BLUE2 = "#285d88"
BLUE3 = "#33719f"
GOLD = "#c8963e"
LIGHT = "#cfe4f4"

BASE_CSS = """
html, body { margin:0; padding:0; width:1200px; height:1200px; overflow:hidden; }
.card { width:1200px; height:1200px; position:relative;
  background: linear-gradient(160deg, %s 0%%, #23364a 42%%, %s 78%%, %s 100%%);
  font-family:"Helvetica Neue", Arial, sans-serif; box-sizing:border-box; }
.path { position:absolute; inset:0; opacity:0.14; }
.brand-row { position:absolute; top:64px; left:0; right:0; display:flex; align-items:center;
  justify-content:center; gap:16px; z-index:2; }
.logo-mark { width:52px; height:52px; filter:invert(1) brightness(2.1); }
.wordmark { line-height:1.05; }
.wordmark .light { display:block; color:#fff; font-weight:300; font-size:24px; letter-spacing:0.02em; }
.wordmark .bold { display:block; color:#fff; font-weight:800; font-size:21px; letter-spacing:0.18em; }
.content { position:absolute; left:0; right:0; top:210px; bottom:150px; display:flex;
  flex-direction:column; align-items:center; justify-content:center; z-index:2; padding:0 90px;
  box-sizing:border-box; }
.rule { width:90px; height:5px; background:%s; border-radius:3px; margin:0 0 28px 0; }
.tagline { position:absolute; bottom:56px; left:0; right:0; text-align:center; color:#9cc4e2;
  font-size:19px; letter-spacing:0.04em; z-index:2; }
""" % (NAVY, BLUE2, BLUE3, GOLD)

PATH_SVG = """<svg class="path" viewBox="0 0 1200 1200" xmlns="http://www.w3.org/2000/svg">
  <path d="M 60 1120 C 260 1120, 260 820, 460 820 S 660 1020, 860 1020 S 1080 700, 1140 620"
        fill="none" stroke="#ffffff" stroke-width="4" stroke-dasharray="1 20" stroke-linecap="round"/>
  <circle cx="60" cy="1120" r="11" fill="#ffffff"/><circle cx="460" cy="820" r="11" fill="#ffffff"/>
  <circle cx="860" cy="1020" r="11" fill="#ffffff"/><circle cx="1140" cy="620" r="14" fill="%s"/>
</svg>""" % GOLD

BRAND_ROW = """<div class="brand-row"><img class="logo-mark" src="%s" />
  <div class="wordmark"><span class="light">CHECKPOINT</span><span class="bold">PLANNING</span></div>
</div>""" % LOGO

def wrap(inner_css, inner_html):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8" /><style>{BASE_CSS}{inner_css}</style></head>
<body><div class="card">{PATH_SVG}{BRAND_ROW}<div class="content">{inner_html}</div>
<p class="tagline">FINANCIAL CLARITY FOR LIFE'S IN-BETWEENS</p></div></body></html>"""

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------------------------------------------------------------------------
# Motif builders
# ---------------------------------------------------------------------------

def quote_motif(line1, line2, subline):
    css = """
    .quote { color:#fff; font-size:56px; font-weight:700; text-align:center; max-width:940px; line-height:1.25; margin:0 0 28px 0; }
    .subline { color:%s; font-size:25px; text-align:center; max-width:780px; line-height:1.5; }
    """ % LIGHT
    html = f'<p class="quote">&ldquo;{line1}<br/>{line2}&rdquo;</p><div class="rule"></div><p class="subline">{subline}</p>'
    return css, html

def checklist_motif(headline, items, subline):
    css = """
    .headline { color:#fff; font-size:38px; font-weight:700; text-align:center; max-width:920px; margin:0 0 34px 0; line-height:1.3; }
    .list { background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.25); border-radius:12px;
            padding:30px 44px; margin-bottom:32px; }
    .item { display:flex; align-items:center; gap:16px; color:#fff; font-size:24px; font-weight:600; padding:11px 0; }
    .check { width:26px; height:26px; border-radius:6px; background:%s; flex-shrink:0; position:relative; }
    .check::after { content:''; position:absolute; left:7px; top:3px; width:8px; height:13px; border:solid #1b2027; border-width:0 3px 3px 0; transform:rotate(40deg); }
    .subline { color:%s; font-size:24px; text-align:center; max-width:760px; line-height:1.5; }
    """ % (GOLD, LIGHT)
    items_html = "".join(f'<div class="item"><span class="check"></span>{i}</div>' for i in items)
    return css, f'<p class="headline">{headline}</p><div class="list">{items_html}</div><p class="subline">{subline}</p>'

def stat_motif(big1, big2, headline, subline):
    css = """
    .statrow { display:flex; align-items:center; gap:44px; margin-bottom:32px; }
    .stat { color:#fff; font-size:118px; font-weight:800; line-height:1; }
    .arrow { color:%s; font-size:48px; }
    .headline { color:#fff; font-size:36px; font-weight:700; text-align:center; max-width:900px; margin:0 0 20px 0; }
    .subline { color:%s; font-size:24px; text-align:center; max-width:760px; line-height:1.5; }
    """ % (GOLD, LIGHT)
    html = f"""<div class="statrow"><span class="stat">{big1}</span><span class="arrow">&rarr;</span>
      <span class="stat" style="color:{GOLD};">{big2}</span></div>
      <p class="headline">{headline}</p><div class="rule"></div><p class="subline">{subline}</p>"""
    return css, html

def roadmap_motif(active_phases, headline, subline):
    phases = ["1", "2", "3", "4", "5"]
    labels = ["Begin", "Protect", "Plot", "Implement", "Track"]
    css = """
    .headline { color:#fff; font-size:34px; font-weight:700; text-align:center; max-width:920px; margin:0 0 54px 0; line-height:1.3; }
    .markers { display:flex; align-items:flex-start; margin-bottom:36px; }
    .marker { display:flex; flex-direction:column; align-items:center; width:64px; }
    .dot { width:30px; height:30px; border-radius:50%%; display:flex; align-items:center; justify-content:center;
           color:#fff; font-weight:800; font-size:15px; border:3px solid rgba(255,255,255,0.5); }
    .dot.active { background:%s; border-color:%s; color:#1b2027; width:38px; height:38px; font-size:17px; }
    .dot.inactive { background:rgba(255,255,255,0.12); }
    .lbl { color:#fff; font-size:14px; font-weight:600; margin-top:10px; opacity:0.75; text-align:center; }
    .lbl.active { opacity:1; font-weight:800; }
    .seg { width:58px; height:3px; background:#ffffff; opacity:0.4; margin-top:17px; }
    .subline { color:%s; font-size:24px; text-align:center; max-width:780px; line-height:1.5; }
    """ % (GOLD, GOLD, LIGHT)
    nodes = []
    for i, (num, lbl) in enumerate(zip(phases, labels)):
        active = (i + 1) in active_phases
        cls = "active" if active else "inactive"
        nodes.append(f'<div class="marker"><div class="dot {cls}">{num}</div><div class="lbl {cls}">{lbl}</div></div>')
        if i < 4:
            nodes.append('<div class="seg"></div>')
    html = f'<p class="headline">{headline}</p><div class="markers">{"".join(nodes)}</div><p class="subline">{subline}</p>'
    return css, html

def photo_motif(quote, subline):
    css = """
    .photorow { display:flex; align-items:center; gap:44px; margin-bottom:32px; }
    .photo-wrap { width:280px; height:280px; border-radius:50%%; overflow:hidden; flex-shrink:0;
                  border:4px solid rgba(255,255,255,0.35); position:relative; }
    .photo-wrap img { width:100%%; height:100%%; object-fit:cover; object-position:center 15%%; }
    .photo-wrap .tint { position:absolute; inset:0; background:linear-gradient(160deg, rgba(27,32,39,0.15) 0%%, rgba(40,93,136,0.35) 100%%); }
    .quote { color:#fff; font-size:34px; font-weight:700; line-height:1.3; max-width:560px; }
    .subline { color:%s; font-size:23px; text-align:center; max-width:820px; line-height:1.5; margin-top:6px; }
    """ % LIGHT
    html = f"""<div class="photorow">
      <div class="photo-wrap"><img src="{HEADSHOT}" /><div class="tint"></div></div>
      <p class="quote">&ldquo;{quote}&rdquo;</p>
    </div><div class="rule"></div><p class="subline">{subline}</p>"""
    return css, html

# ---------------------------------------------------------------------------
# 12 posts, mapped to motifs
# ---------------------------------------------------------------------------

POSTS = {
    1: roadmap_motif([1], "The Checkpoint Strategy, Phase 1", "Where We Begin: a complimentary conversation before any plan gets built."),
    2: checklist_motif("Job Loss: The First 30 Days",
        ["Confirm severance details", "Understand your COBRA window", "Pause the big decisions"],
        "Stability first. The plan comes after."),
    3: quote_motif("It's not a marketing word.", "It's a legal standard.",
        "What “fiduciary” actually means, and the standard I'm held to."),
    4: roadmap_motif([2], "The Checkpoint Strategy, Phase 2", "Identify and Protect: stabilizing the present before building toward the future."),
    5: stat_motif("62", "70", "It's Not Just About the Number.",
        "Claiming Social Security early can permanently cut your benefit 25 to 30 percent."),
    6: photo_motif("Progress happens through checkpoints, not one big push.",
        "What competitive endurance racing taught me about financial planning."),
    7: roadmap_motif([3], "The Checkpoint Strategy, Phase 3", "Plot Checkpoints: milestones at 30, 90, and 180 days, not one distant goal."),
    8: checklist_motif("Know the Real Value of a Settlement",
        ["Tax treatment by account type", "Retirement dollars vs. home equity", "The after-tax total, not the headline number"],
        "Two settlements with the same total can leave very different pictures."),
    9: photo_motif("You work directly with me. Every meeting, every review.",
        "Not a junior associate. Not a call center. Me, for as long as we work together."),
    10: roadmap_motif([4, 5], "The Checkpoint Strategy, Phase 4 and 5", "Implement, then Track and Reset. Five phases, one process, the same structure every time."),
    11: checklist_motif("Inheritance: Don't Lose Track of This",
        ["The step-up in cost basis", "Date-of-death value, documented", "No need to decide anything quickly"],
        "One detail that can significantly reduce, or eliminate, capital gains tax."),
    12: quote_motif("One checkpoint", "at a time.",
        "The thread through everything this month: the strategy, the story, and the decisions in between."),
}

def render(num, css, html):
    full_html = wrap(css, html)
    tmp_html = os.path.join(OUT_DIR, f"_post_{num:02d}.html")
    with open(tmp_html, "w") as f:
        f.write(full_html)
    raw_path = os.path.join(OUT_DIR, f"_post_{num:02d}_raw.png")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH if os.path.exists(CHROME_PATH) else None)
        page = browser.new_page(viewport={"width": 1200, "height": 1200}, device_scale_factor=2)
        page.goto(f"file://{tmp_html}")
        page.wait_for_timeout(150)
        page.screenshot(path=raw_path)
        browser.close()
    img = Image.open(raw_path).resize((1200, 1200), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, f"post-{num:02d}.png")
    img.save(out_path)
    os.remove(tmp_html)
    os.remove(raw_path)
    print("wrote", out_path)

if __name__ == "__main__":
    for num, (css, html) in POSTS.items():
        render(num, css, html)
