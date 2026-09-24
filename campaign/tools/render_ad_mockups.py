# Renders 8 LinkedIn Sponsored Content mockups, one per ad variant in
# campaign/02-linkedin-ads.md, showing the ad exactly as it will appear in
# the LinkedIn feed: company row, intro text with "...see more" truncation,
# the real ad creative image, headline/description footer, and CTA button.
# Copy below is copied verbatim from 02-linkedin-ads.md, keep them in sync
# if that file changes.
#
# Requires: pip install playwright pillow.
# Usage: python3 campaign/tools/render_ad_mockups.py

import os
import re
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAMPAIGN = os.path.join(ROOT, "campaign")
CREATIVE_DIR = os.path.join(CAMPAIGN, "assets", "ad-creatives")
MOCKUP_DIR = os.path.join(CAMPAIGN, "assets", "ad-mockups")
CHROME_PATH = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")

ADS = [
    dict(name="job-loss-a1", segment="Job Loss & Layoff, Variant A1", creative="job-loss-a1-quote.png",
        intro="A layoff puts a dozen financial decisions in front of you at once, including severance, COBRA, and your old 401(k), usually the week you can least afford to rush them. Get a free 90-day workbook built to help you slow down and know what to do first.",
        headline="Just Lost Your Job? Get a Clear 90-Day Plan.",
        desc="Free workbook + a complimentary planning session. No cost, no obligation.", cta="Download"),
    dict(name="job-loss-a2", segment="Job Loss & Layoff, Variant A2", creative="job-loss-a2-workbook.png",
        intro="Severance decisions. COBRA vs. marketplace coverage. What to do with your old 401(k). These don't have to be solved this week, but they do need a plan. Checkpoint Planning built a free workbook specifically for people navigating a layoff.",
        headline="A 90-Day Plan for Your Next Chapter",
        desc="Free “Your Next Checkpoint” workbook. Fiduciary guidance, not a sales pitch.", cta="Download"),
    dict(name="early-retirement-a1", segment="Early Retirement, Variant A1", creative="early-retirement-a1-roadmap.png",
        intro="Retiring earlier than planned changes the math: Social Security timing, healthcare before Medicare, pension elections, and portfolio longevity. Before you commit to a date, get the free Early Retirement Checkpoint Guide and pressure-test the plan.",
        headline="Retiring Early? Make Sure Your Money Can Too.",
        desc="Free guide + a complimentary session with a CRPC™ planner.", cta="Download"),
    dict(name="early-retirement-a2", segment="Early Retirement, Variant A2", creative="early-retirement-a2-stat.png",
        intro="Claiming Social Security at 62 instead of full retirement age can permanently cut your benefit by 25-30%. If your retirement timeline moved up, by choice or otherwise, this is the decision worth getting right before you file anything.",
        headline="The Retirement Decisions That Don't Wait",
        desc="Free Early Retirement Checkpoint Guide. No cost, no obligation session.", cta="Download"),
    dict(name="divorce-a1", segment="Divorce, Variant A1", creative="divorce-a1-checklist.png",
        intro="Divorce brings a wave of financial decisions on top of an already difficult time: settlement analysis, QDROs, tax filing status, rebuilding a budget on your own. A free guide on what to understand before you sign anything.",
        headline="Financial Clarity Before You Sign a Settlement",
        desc="Free Divorce Financial Checkpoint Guide. Confidential.", cta="Download"),
    dict(name="inheritance-a1", segment="Inheritance & Unexpected Wealth, Variant A1", creative="inheritance-a1-quote.png",
        intro="Received an inheritance? There's rarely a need to decide anything quickly. A free guide covering inherited IRA rules, tax basics, and the questions worth asking before you invest, spend, or sell.",
        headline="Slow Down Before You Decide Anything",
        desc="Free Inheritance Checkpoint Guide. No pressure, no obligation.", cta="Download"),
]

TEMPLATE = """<!DOCTYPE html><html><head><meta charset="UTF-8" />
<style>
  html, body { margin:0; padding:0; background:#e9eef2; }
  .card { width:1200px; background:#ffffff; font-family:"Helvetica Neue", Arial, sans-serif;
          box-shadow:0 1px 2px rgba(0,0,0,0.15); box-sizing:border-box; }
  .header { display:flex; align-items:flex-start; gap:14px; padding:22px 26px 14px 26px; }
  .logo { width:56px; height:56px; border-radius:50%%; background:#000000; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
  .logo img { width:32px; height:32px; }
  .who { line-height:1.35; }
  .who .name { font-size:18px; font-weight:700; color:#1b2027; }
  .who .promoted { font-size:14px; color:#5a6570; display:flex; align-items:center; gap:5px; }
  .intro { padding:0 26px 20px 26px; font-size:17px; line-height:1.5; color:#232a30; }
  .intro .see-more { color:#5a6570; font-weight:600; }
  .adimg { width:1200px; display:block; }
  .footer { background:#f4f6f8; padding:18px 26px; display:flex; align-items:center; justify-content:space-between; border-top:1px solid #e2e7eb; }
  .footer .text { max-width:900px; }
  .footer .domain { font-size:13px; color:#5a6570; text-transform:uppercase; letter-spacing:0.03em; margin-bottom:4px; }
  .footer .headline { font-size:19px; font-weight:700; color:#1b2027; margin-bottom:4px; }
  .footer .desc { font-size:15px; color:#5a6570; }
  .cta { background:#e9eef2; color:#1b2027; font-size:16px; font-weight:700; border:1.5px solid #1b2027;
         border-radius:24px; padding:11px 28px; flex-shrink:0; margin-left:24px; }
  .engage { display:flex; gap:34px; padding:14px 26px; color:#5a6570; font-size:15px; font-weight:600; border-top:1px solid #eef1f3; }
  .badge { position:absolute; margin-left:-72px; margin-top:60px; background:#1b2027; color:#fff; font-size:11px;
           font-weight:700; letter-spacing:0.06em; padding:3px 8px; border-radius:4px; }
</style></head>
<body>
<div class="card">
  <div class="header">
    <div class="logo"><img src="../../../website/assets/checkpoint-mark-white.png" /></div>
    <div class="who">
      <div class="name">Checkpoint Planning</div>
      <div class="promoted">&#128274; Promoted</div>
    </div>
  </div>
  <div class="intro">%s <span class="see-more">&hellip;see more</span></div>
  <img class="adimg" src="../ad-creatives/%s" />
  <div class="footer">
    <div class="text">
      <div class="domain">checkpointplanning.com</div>
      <div class="headline">%s</div>
      <div class="desc">%s</div>
    </div>
    <button class="cta">%s</button>
  </div>
  <div class="engage"><span>&#128077; Like</span><span>&#128172; Comment</span><span>&#8617; Share</span><span>&#9993; Send</span></div>
</div>
</body></html>"""

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render(ad):
    html = TEMPLATE % (esc(ad["intro"]), ad["creative"], esc(ad["headline"]), esc(ad["desc"]), esc(ad["cta"]))
    tmp_html = os.path.join(MOCKUP_DIR, f"_{ad['name']}.html")
    with open(tmp_html, "w") as f:
        f.write(html)
    out_path = os.path.join(MOCKUP_DIR, f"{ad['name']}.png")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH if os.path.exists(CHROME_PATH) else None)
        page = browser.new_page(viewport={"width": 1200, "height": 900}, device_scale_factor=2)
        page.goto(f"file://{tmp_html}")
        page.wait_for_timeout(150)
        page.screenshot(path=out_path, full_page=True)
        browser.close()
    os.remove(tmp_html)
    print("wrote", out_path, "--", ad["segment"])

if __name__ == "__main__":
    for ad in ADS:
        render(ad)
