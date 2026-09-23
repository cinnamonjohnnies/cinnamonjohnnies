# Converts the 12 Month 1 posts from single quote-cards into LinkedIn
# "document" carousel posts (the format LinkedIn's own document-post data
# shows getting meaningfully higher engagement than single-image posts,
# see campaign/08-linkedin-content-calendar-month1.md intro for the
# rationale). Each post becomes a 4-5 slide PDF, uploaded to LinkedIn as a
# document post, one page per swipeable slide, 1080x1080.
#
# All body copy is reused verbatim from each post's own approved text in
# campaign/08-linkedin-content-calendar-month1.md, just re-flowed across
# slides plus a consistent title/CTA wrapper. No new claims are introduced.
#
# Output per post: campaign/assets/post-carousels/post-NN/slide-0X.png
# (individual slides, for reference/re-editing) and
# campaign/assets/post-carousels/post-NN.pdf (the file to actually upload
# to LinkedIn as the document post).
#
# Requires: pip install playwright pillow pypdf.
# Usage: python3 campaign/tools/render_post_carousels.py

import os
from playwright.sync_api import sync_playwright
from PIL import Image
from pypdf import PdfWriter
import img2pdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAMPAIGN = os.path.join(ROOT, "campaign")
OUT_DIR = os.path.join(CAMPAIGN, "assets", "post-carousels")
CHROME_PATH = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
LOGO = "../../../../website/assets/checkpoint-mark-white.png"
HEADSHOT = "../../../../website/assets/scott-marcoe.jpg"

BLACK = "#000000"
CHARCOAL = "#3e3e3e"
TEAL = "#2e86ab"
ON_DARK_MUTED = "#e3e3e3"
LINK_ON_DARK = "#7cc3df"

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Roboto:wght@400;600;700&display=swap" rel="stylesheet" />'

BASE_CSS = """
html, body { margin:0; padding:0; width:1080px; height:1080px; overflow:hidden; }
.card { width:1080px; height:1080px; position:relative;
  background: linear-gradient(160deg, %s 0%%, %s 100%%);
  font-family:"Roboto", Arial, sans-serif; box-sizing:border-box; }
.top-row { position:absolute; top:50px; left:56px; right:56px; display:flex; align-items:center;
  justify-content:space-between; z-index:2; }
.brand { display:flex; align-items:center; gap:10px; }
.logo-mark { width:34px; height:34px; }
.brand-word { color:#fff; font-family:"Montserrat", Arial, sans-serif; font-weight:800; font-size:15px; letter-spacing:0.14em; }
.kicker { color:%s; font-weight:700; font-size:15px; letter-spacing:0.12em; text-transform:uppercase; }
.dots { position:absolute; bottom:46px; left:0; right:0; display:flex; justify-content:center; gap:9px; z-index:2; }
.dot { width:8px; height:8px; border-radius:50%%; background:rgba(255,255,255,0.35); }
.dot.on { background:%s; width:22px; border-radius:4px; }
.pagenum { position:absolute; bottom:46px; right:56px; color:rgba(255,255,255,0.55); font-size:15px; font-weight:600; z-index:2; }
.rule { width:80px; height:4px; background:%s; border-radius:2px; margin:0 0 26px 0; }
""" % (BLACK, CHARCOAL, LINK_ON_DARK, TEAL, TEAL)

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def top_row(kicker):
    return f"""<div class="top-row">
      <div class="brand"><img class="logo-mark" src="{LOGO}" /><span class="brand-word">CHECKPOINT</span></div>
      <div class="kicker">{esc(kicker)}</div>
    </div>"""

def dots(n_total, active_idx):
    ds = "".join(f'<div class="dot {"on" if i == active_idx else ""}"></div>' for i in range(n_total))
    return f'<div class="dots">{ds}</div>'

def title_slide(kicker, headline, subtext, n_total, photo=False):
    css = """
    .content { position:absolute; left:0; right:0; top:0; bottom:0; display:flex; flex-direction:column;
      align-items:center; justify-content:center; z-index:2; padding:0 96px; box-sizing:border-box; text-align:center; }
    .headline { color:#fff; font-family:"Montserrat", Arial, sans-serif; font-size:58px; font-weight:800; line-height:1.2; margin:0 0 24px 0; }
    .subtext { color:%s; font-size:26px; line-height:1.5; max-width:820px; }
    .swipe { position:absolute; bottom:100px; left:0; right:0; text-align:center; color:rgba(255,255,255,0.5);
      font-size:16px; letter-spacing:0.08em; z-index:2; }
    .photo-wrap { width:210px; height:210px; border-radius:50%%; overflow:hidden; margin:0 auto 30px auto;
      border:4px solid rgba(255,255,255,0.35); position:relative; }
    .photo-wrap img { width:100%%; height:100%%; object-fit:cover; object-position:center 15%%; }
    .photo-wrap .tint { position:absolute; inset:0; background:linear-gradient(160deg, rgba(0,0,0,0.15) 0%%, rgba(46,134,171,0.35) 100%%); }
    """ % ON_DARK_MUTED
    photo_html = f'<div class="photo-wrap"><img src="{HEADSHOT}" /><div class="tint"></div></div>' if photo else ""
    html = f"""<div class="content">{photo_html}<p class="headline">{headline}</p>
      <p class="subtext">{subtext}</p></div><p class="swipe">SWIPE &rarr;</p>{dots(n_total, 0)}"""
    return css, top_row(kicker), html

def content_slide(body, idx, n_total, kicker):
    css = """
    .content { position:absolute; left:0; right:0; top:0; bottom:0; display:flex; align-items:center;
      justify-content:center; z-index:2; padding:0 100px; box-sizing:border-box; }
    .body { color:#fff; font-size:40px; font-weight:600; line-height:1.45; text-align:left; max-width:880px; }
    .body b { color:%s; font-family:"Montserrat", Arial, sans-serif; }
    """ % LINK_ON_DARK
    html = f'<div class="content"><p class="body">{body}</p></div>{dots(n_total, idx)}<div class="pagenum">{idx+1}/{n_total}</div>'
    return css, top_row(kicker), html

def close_slide(takeaway, cta, n_total, kicker):
    css = """
    .content { position:absolute; left:0; right:0; top:0; bottom:0; display:flex; flex-direction:column;
      align-items:center; justify-content:center; z-index:2; padding:0 96px; box-sizing:border-box; text-align:center; }
    .takeaway { color:#fff; font-family:"Montserrat", Arial, sans-serif; font-size:42px; font-weight:800; line-height:1.3; margin:0 0 26px 0; max-width:820px; }
    .cta { color:%s; font-size:24px; line-height:1.5; max-width:760px; }
    """ % ON_DARK_MUTED
    html = f"""<div class="content"><p class="takeaway">&ldquo;{takeaway}&rdquo;</p><div class="rule"></div>
      <p class="cta">{cta}</p></div>{dots(n_total, n_total - 1)}"""
    return css, top_row(kicker), html

def wrap(inner_css, top_row_html, inner_html):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8" />{FONT_LINK}<style>{BASE_CSS}{inner_css}</style></head>
<body><div class="card">{top_row_html}{inner_html}</div></body></html>"""

# ---------------------------------------------------------------------------
# 12 posts, each a list of slide-builder outputs (css, top_row_html, html)
# ---------------------------------------------------------------------------

CTA_STANDARD = "The Where We Begin conversation is complimentary and carries no obligation. Link in the comments."

def phase_carousel(post_num, part_label, phase_title, paras, takeaway):
    n = len(paras) + 2
    slides = [title_slide(f"CHECKPOINT STRATEGY • {part_label}", phase_title, "A five-phase framework for navigating major financial transitions.", n)]
    for i, p in enumerate(paras):
        slides.append(content_slide(p, i + 1, n, f"CHECKPOINT STRATEGY • {part_label}"))
    slides.append(close_slide(takeaway, CTA_STANDARD, n, f"CHECKPOINT STRATEGY • {part_label}"))
    return slides

def topic_carousel(post_num, kicker, headline, subtext, paras, takeaway, cta=CTA_STANDARD, photo=False):
    n = len(paras) + 2
    slides = [title_slide(kicker, headline, subtext, n, photo=photo)]
    for i, p in enumerate(paras):
        slides.append(content_slide(p, i + 1, n, kicker))
    slides.append(close_slide(takeaway, cta, n, kicker))
    return slides

POSTS = {
    1: phase_carousel(1, "Part 1 of 5", "Phase 1:<br/>Where We Begin",
        ["Before any plan gets built, there's a conversation. Not a sales pitch, not a form to fill out, just 45 minutes to understand what's actually changing in your life and what feels most uncertain about it.",
         "This is where every client relationship starts, and it's complimentary regardless of what happens after. Sometimes that conversation confirms we're a good fit. Sometimes it doesn't, and I'll tell you that too."],
        "Clarity has to come before a plan means anything."),

    2: topic_carousel(2, "JOB LOSS & LAYOFF", "The First 30 Days", "What actually matters after a layoff, in order.",
        ["<b>1. Confirm your severance details.</b><br/>How it's paid, and whether it affects unemployment eligibility.",
         "<b>2. Understand your benefits deadlines.</b><br/>COBRA elections typically have a 60-day window, not a 60-day requirement to decide immediately.",
         "<b>3. Then stop.</b><br/>Nothing about your 401(k), a major purchase, or a big financial decision needs to happen this week."],
        "The goal of the first month isn't a plan. It's stability."),

    3: topic_carousel(3, "FIDUCIARY ADVISOR", "What “Fiduciary”<br/>Actually Means", "Beyond the buzzword, this is a legal standard.",
        ["It means I'm legally required to act in your best interest, not the firm's, not a product manufacturer's, and not my own. Every recommendation has to clear that bar.",
         "It means no sales quotas and no proprietary products I'm incentivized to push. When insurance or annuity products do carry a commission, that's disclosed to you in writing before any recommendation."],
        "It's not a marketing word here. It's a legal standard."),

    4: phase_carousel(4, "Part 2 of 5", "Phase 2:<br/>Identify and Protect",
        ["Before building toward the future, we stabilize the present. That means reviewing benefits continuation, checking for insurance gaps, and confirming cash flow can hold steady through the transition.",
         "This is the phase most people want to skip past, they want the plan, the strategy, the exciting part. But a plan built on an unstable foundation doesn't hold up."],
        "Protecting what you already have comes before growing it."),

    5: topic_carousel(5, "EARLY RETIREMENT", "62 vs. 70", "The Social Security decision that's easy to get wrong.",
        ["Claiming Social Security at 62 instead of your full retirement age can permanently reduce your monthly benefit by roughly 25 to 30 percent. Waiting until 70 increases it.",
         "I see the same mistake often: claiming early simply because retirement started early, without ever running the numbers on the alternative."],
        "Retiring earlier than planned doesn't mean you have to claim earlier than planned."),

    6: topic_carousel(6, "THE NAME BEHIND THE NAME", "What Endurance Racing<br/>Taught Me", "A question I get asked often.",
        ["I'm a state champion mountain bike racer and a national champion in 24-hour endurance racing. Training for those races never came down to one big effort.",
         "It came down to breaking an enormous challenge into checkpoints, and adjusting to real conditions along the way, weather, terrain, how my body actually felt that day versus the plan on paper."],
        "Progress happens through checkpoints, pacing, and smart decisions made under real circumstances.",
        cta="That's where the name, and the whole approach, comes from.", photo=True),

    7: phase_carousel(7, "Part 3 of 5", "Phase 3:<br/>Plot Checkpoints",
        ["This is where the actual plan gets built, with milestones set at 30, 90, and 180 days rather than one distant, abstract goal.",
         "Shorter checkpoints make progress visible sooner, and create natural points to adjust when real life doesn't match the projection, which it usually doesn't.",
         "Coordination with your CPA or attorney happens here too, when the situation calls for it, so the plan reflects your whole financial picture."],
        "This is where the actual plan gets built."),

    8: topic_carousel(8, "DIVORCE", "The Real Value<br/>of a Settlement", "What the headline number hides.",
        ["A dollar in a Roth IRA, a dollar in a traditional 401(k), and a dollar of home equity carry different tax treatment and different liquidity.",
         "Two settlements with the same total can leave two very different financial pictures once that's accounted for."],
        "Understand the real, after-tax value of what's on the table before you sign."),

    9: topic_carousel(9, "HOW THIS PRACTICE WORKS", "You Work Directly<br/>With Me", "Something worth saying plainly.",
        ["Every meeting, every review, every planning conversation.",
         "Not a junior associate after the first meeting. Not a call center for questions. Me, for as long as we work together."],
        "A financial plan is a personal thing, and the relationship behind it should be too.", photo=True),

    10: phase_carousel(10, "Part 4 & 5 of 5", "Implement,<br/>Track and Reset",
        ["<b>Phase 4: Implement.</b><br/>Recommendations become action: account rollovers, portfolio construction, document updates, and referrals to specialists.",
         "<b>Phase 5: Track and Reset.</b><br/>Life doesn't hold still after a plan is built. Ongoing reviews and recalibration keep the plan aligned as things change."],
        "Five phases, one process, the same structure every time."),

    11: topic_carousel(11, "INHERITANCE", "The Step-Up<br/>in Cost Basis", "One detail worth knowing, and confirming early.",
        ["Inherited stocks, funds, or real estate typically receive a “step-up” in cost basis to their value on the date of death.",
         "That single detail can significantly reduce, or eliminate, capital gains tax if you sell. It's also one of the easiest things to lose track of if records aren't documented early."],
        "Almost nothing about an inheritance needs to be decided quickly."),

    12: topic_carousel(12, "MONTH ONE, A RECAP", "One Checkpoint<br/>at a Time", "The thread through everything this month.",
        ["The strategy, the story behind it, and the specific decisions that come with a layoff, an early retirement, a divorce, or an inheritance.",
         "None of these moments come with a manual. What they need is a structured process and someone who works only for you while you're in the middle of it."],
        "If you or someone you know is navigating one of these transitions, let's talk."),
}

def render_slide(post_num, slide_idx, css, top_row_html, html, slide_dir):
    full_html = wrap(css, top_row_html, html)
    tmp_html = os.path.join(slide_dir, f"_slide_{slide_idx:02d}.html")
    with open(tmp_html, "w") as f:
        f.write(full_html)
    raw_path = os.path.join(slide_dir, f"_slide_{slide_idx:02d}_raw.png")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH if os.path.exists(CHROME_PATH) else None)
        page = browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        page.goto(f"file://{tmp_html}")
        page.wait_for_timeout(350)
        page.screenshot(path=raw_path)
        browser.close()
    img = Image.open(raw_path).resize((1080, 1080), Image.LANCZOS)
    out_path = os.path.join(slide_dir, f"slide-{slide_idx:02d}.png")
    img.save(out_path)
    os.remove(tmp_html)
    os.remove(raw_path)
    return out_path

if __name__ == "__main__":
    for post_num, slides in POSTS.items():
        slide_dir = os.path.join(OUT_DIR, f"post-{post_num:02d}")
        os.makedirs(slide_dir, exist_ok=True)
        slide_paths = []
        for i, (css, top_row_html, html) in enumerate(slides):
            slide_paths.append(render_slide(post_num, i + 1, css, top_row_html, html, slide_dir))
        pdf_path = os.path.join(OUT_DIR, f"post-{post_num:02d}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(slide_paths))
        print(f"post {post_num}: {len(slide_paths)} slides -> {pdf_path}")
