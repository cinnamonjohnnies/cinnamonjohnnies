# Renders 12 LinkedIn organic post mockups, one per post in
# campaign/08-linkedin-content-calendar-month1.md, showing the post exactly
# as it will appear in-feed: profile row, full post text with hashtags and
# disclosure line, the quote-card image, and the engagement bar. Parses the
# calendar file directly so it stays in sync with edits there.
#
# Requires: pip install playwright.
# Usage: python3 campaign/tools/render_post_mockups.py

import os
import re
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAMPAIGN = os.path.join(ROOT, "campaign")
OUT_DIR = os.path.join(CAMPAIGN, "assets", "post-mockups")
CHROME_PATH = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")

DISCLOSURE_FULL = (
    "Scott Marcoe offers products and services using the following business names: "
    "Checkpoint Planning, Capstone Financial Group, insurance and financial services. "
    "Ameritas Investment Company, LLC (AIC), Member FINRA/SIPC, securities and investments. "
    "Ameritas Advisory Services, LLC (AAS), investment advisory services. AIC and AAS are "
    "not affiliated with Capstone Financial Group."
)

with open(os.path.join(CAMPAIGN, "08-linkedin-content-calendar-month1.md")) as f:
    cal_text = f.read()

post_blocks = re.findall(r"## Post (\d+), ([^\n]+)\n\n(.*?)(?=\n---\n\n## Post|\Z)", cal_text, re.S)

DATES = {
    1: "Mon • Sep 28", 2: "Wed • Sep 30", 3: "Fri • Oct 2", 4: "Mon • Oct 5",
    5: "Wed • Oct 7", 6: "Fri • Oct 9", 7: "Mon • Oct 12", 8: "Wed • Oct 14",
    9: "Fri • Oct 16", 10: "Mon • Oct 19", 11: "Wed • Oct 21", 12: "Fri • Oct 23",
}

TEMPLATE = """<!DOCTYPE html><html><head><meta charset="UTF-8" /><style>
  html, body { margin:0; padding:0; background:#e9eef2; }
  .card { width:1200px; background:#ffffff; font-family:"Helvetica Neue", Arial, sans-serif;
          box-shadow:0 1px 2px rgba(0,0,0,0.15); box-sizing:border-box; }
  .header { display:flex; align-items:flex-start; gap:14px; padding:22px 26px 16px 26px; }
  .avatar { width:56px; height:56px; border-radius:50%%; object-fit:cover; flex-shrink:0; }
  .who .name { font-size:18px; font-weight:700; color:#1b2027; }
  .who .headline { font-size:14px; color:#3a444d; max-width:820px; }
  .who .meta { font-size:13px; color:#5a6570; margin-top:2px; }
  .body { padding:0 26px 22px 26px; font-size:17px; line-height:1.6; color:#232a30; white-space:pre-wrap; }
  .body .hashtags { color:#2860a3; }
  .body .disclosure { font-size:13px; color:#5a6570; line-height:1.5; margin-top:16px; }
  .postimg { width:1200px; display:block; }
  .engage { display:flex; gap:34px; padding:16px 26px; color:#5a6570; font-size:15px; font-weight:600; border-top:1px solid #eef1f3; }
</style></head>
<body>
<div class="card">
  <div class="header">
    <img class="avatar" src="scott-marcoe.jpg" />
    <div class="who">
      <div class="name">Scott Marcoe, CRPC&trade;</div>
      <div class="headline">Founder &amp; Financial Planner, Checkpoint Planning | Fiduciary Advisor for Life Transitions</div>
      <div class="meta">%s &nbsp;&middot;&nbsp; &#127760;</div>
    </div>
  </div>
  <div class="body">%s</div>
  <img class="postimg" src="../post-creatives/post-%02d.png" />
  <div class="engage"><span>&#128077; Like</span><span>&#128172; Comment</span><span>&#8617; Share</span><span>&#9993; Send</span></div>
</div>
</body></html>"""

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def format_body(raw):
    raw = raw.strip()
    paras = re.split(r"\n\n+", raw)
    out = []
    for para in paras:
        para = para.strip()
        if para.startswith("**Disclosure:**"):
            out.append(f'<div class="disclosure">{esc(DISCLOSURE_FULL)}</div>')
        elif para.startswith("#"):
            out.append(f'<div class="hashtags">{esc(para)}</div>')
        else:
            # bold phase labels like **Phase 1: Where We Begin.**
            p = esc(para)
            p = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", p)
            out.append(f"<p style='margin:0 0 14px 0;'>{p}</p>")
    return "".join(out)

def render(num, headline, body_text):
    body_html = format_body(body_text)
    html = TEMPLATE % (DATES[num], body_html, num)
    tmp_html = os.path.join(OUT_DIR, f"_post_{num:02d}.html")
    with open(tmp_html, "w") as f:
        f.write(html)
    out_path = os.path.join(OUT_DIR, f"post-{num:02d}.png")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH if os.path.exists(CHROME_PATH) else None)
        page = browser.new_page(viewport={"width": 1200, "height": 1000}, device_scale_factor=2)
        page.goto(f"file://{tmp_html}")
        page.wait_for_timeout(150)
        page.screenshot(path=out_path, full_page=True)
        browser.close()
    os.remove(tmp_html)
    print("wrote", out_path)

if __name__ == "__main__":
    for num, headline, body in post_blocks:
        render(int(num), headline.strip(), body)
