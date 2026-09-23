# Creative Brief: LinkedIn Month 1 Visual Design

**Superseded 2026-09-23.** Scott built a real "Checkpoint Planning"
Claude Design System from checkpointplanning.com's actual brand (colors,
logo, icons, and real photography), and that's now applied across the
website and this campaign's creative, see
`website/WEBSITE-REFERENCE.md` for the current brand system and
`campaign/assets/ad-creatives/` and `campaign/assets/post-carousels/`
for the rebuilt, photo-forward creative. The "Brand system" section
below describes the earlier invented navy/gold palette and is now
stale, kept for history rather than deleted. The segment-by-segment
emotional direction further down is still a useful reference for future
creative decisions, that guidance doesn't depend on the old palette.

Original framing (now moot, the design system resolved this): handoff
document for a separate design project, so this repo could stay focused
on strategy, the website, and campaign mechanics while visual design
moved to a dedicated design tool. That's no longer necessary since the
design system provided real assets to build from directly.

## Why this brief exists

The current creative (`campaign/assets/ad-creatives/`,
`campaign/assets/post-carousels/`) is functional, on-brand, and good
enough to submit to compliance, but it reads as competent financial
graphic design, not something that stops a scroll or creates an
emotional connection. It's built entirely from HTML/CSS rendered
programmatically, which is reliable for brand consistency but caps out
on the kind of visual storytelling a designer working directly in
Photoshop, Illustrator, or Premiere can do. That's the gap this brief
hands off.

## The core creative problem to solve

**Every one of these audiences is mid-crisis or mid-transition when they
see this content.** A layoff, a divorce, retiring earlier than planned,
an inheritance after a loss, these are emotional moments before they're
financial ones. The current creative leads with the financial logic
(a stat, a checklist, a workbook) and treats the emotional reality as
background texture. It should be the other way around: **lead with the
feeling, let the financial specifics be the proof point that follows.**

Concretely, that means:

- **The first half-second of visual impact should read as human and
  emotional, not corporate and informational.** A real, unposed-feeling
  moment (not a stock-photo handshake or a growth-arrow icon) does more
  work than any headline.
- **Avoid financial-services visual clichés**: growth arrows, piggy
  banks, handshakes, generic "confident couple looking at a laptop"
  stock photography, coins/dollar signs as decoration.
- **Let each segment's specific emotional truth show up in the visual**,
  not just the copy (see segment-by-segment notes below). Right now all
  four segments share one visual language differentiated only by which
  stat or checklist sits on screen. That's the thing most worth fixing.
- **Scott's own photography is the strongest asset available** and is
  underused. Real, warm, specific beats polished and generic here.

## Brand system (fixed, carry over exactly)

- **Colors**: navy `#1b2027`, `#252b33`, `#394452`; blue `#285d88`,
  `#33719f`, `#4c8cbe`, light blue `#9cc4e2`, `#e7eff6`; gold accent
  `#c8963e` (CTA/highlight only, used sparingly); ink text `#232a30` /
  `#57626c`. Full palette in `website/styles.css`.
- **Logo**: `website/assets/checkpoint-logo-full.png` (full lockup),
  `website/assets/checkpoint-logo-mark.png` (mark only, used inverted
  white-on-dark throughout the campaign creative).
- **Photography**: `website/assets/scott-marcoe.jpg` is the only
  existing photo asset. New, better photography of Scott (candid,
  varied settings/poses, not just the studio headshot) would raise the
  ceiling on every ad and the two personal-story carousel posts
  significantly, this is probably the single highest-leverage thing a
  photographer or the Adobe tools could add.
- **Typography**: Helvetica Neue / system sans in the current build, not
  a locked brand requirement, a designer's typeface choice is welcome as
  long as it stays clean, confident, and legible at small sizes (mobile
  feed).
- **Tone of voice**: direct, calm, no jargon, no urgency/pressure
  tactics, no em dashes anywhere (house rule, applies to any on-image
  text too).

## Hard constraints, do not change without flagging it back

- **Copy is compliance-approved.** Every word in the "Approved copy"
  sections below (headlines, intro text, descriptions, CTAs, post body
  text, hashtags, disclosure line) has been cleared for Ameritas
  compliance submission. If new creative direction requires different
  wording (a shorter headline, a different hook), that's fine, but it
  needs to route back through compliance before anything publishes, it
  can't just ship.
- **The FINRA disclosure line is required on every organic post** (not
  on ads, LinkedIn ad character limits don't allow it and it's covered
  by the landing page instead): "Scott Marcoe offers products and
  services using the following business names: Checkpoint Planning,
  Capstone Financial Group, insurance and financial services. Ameritas
  Investment Company, LLC (AIC), Member FINRA/SIPC, securities and
  investments. Ameritas Advisory Services, LLC (AAS), investment
  advisory services. AIC and AAS are not affiliated with Capstone
  Financial Group."
- **Imagery restrictions by segment** (compliance-driven, already
  reflected in the current copy's "Image concept" notes):
  - Divorce: no imagery implying relationship conflict. Neutral,
    dignified, composed.
  - Inheritance: no imagery referencing loss, grief, or a funeral. Lead
    with the financial-decision moment, not the emotional cause of it.
  - No client testimonials or specific-outcome claims in any visual
    (compliance/privacy issue).
  - No performance claims or anything that reads as investment advice
    rather than education.
- **Destination URLs and UTM parameters are fixed** and must appear
  unchanged wherever the design workflow needs to know the link target
  (see each ad's Destination below). Don't regenerate or simplify them.

## Deliverable specs

### A. 6 LinkedIn single-image ads

- **Size**: 1200 x 627px (LinkedIn's single-image Sponsored Content
  spec), PNG or JPG.
- **Safe area**: keep essential text/logo away from the outer ~40px on
  all sides, LinkedIn's ad unit sometimes crops slightly on mobile
  placements.
- **File naming**: match the existing slugs so they drop back into
  `campaign/assets/ad-creatives/` cleanly: `job-loss-a1-quote.png`,
  `job-loss-a2-workbook.png`, `early-retirement-a1-roadmap.png`,
  `early-retirement-a2-stat.png`, `divorce-a1-checklist.png`,
  `inheritance-a1-quote.png`.

### B. 12 LinkedIn document (carousel) posts

- **Size**: 1080 x 1080px per slide (square), 4-5 slides per post,
  delivered as one PDF per post (LinkedIn uploads document posts as a
  single PDF, each page becomes a swipeable slide).
- **Why carousels, not single images**: LinkedIn's own engagement data
  shows document/carousel posts meaningfully outperform single-image
  posts (roughly 3x engagement in third-party studies), this format
  choice is already locked in, the redesign is about what's on each
  slide, not the format itself.
- **File naming**: `post-01.pdf` through `post-12.pdf`, dropping into
  `campaign/assets/post-carousels/`.

## Segment-by-segment creative direction

### Job Loss & Layoff
**Emotional truth**: the ground just moved. Anxiety, a sense of too many
decisions at once, and underneath it, the need to feel steady again.
**Direction**: visuals that evoke exhaling, steadying, the first calm
moment after the shock, not a workbook cover or a checklist. Think quiet
morning light, a single grounded figure, negative space, rather than
busy financial iconography.

**Approved copy, A1**
Destination: `https://start.checkpointplanning.com/job-loss.html?utm_source=linkedin&utm_medium=paid_social&utm_campaign=cp_jobloss_{yyyy-mm}&utm_content=li_a1`
- Intro text: "A layoff puts a dozen financial decisions in front of you at once, including severance, COBRA, and your old 401(k), usually the week you can least afford to rush them. Get a free 90-day workbook built to help you slow down and know what to do first."
- Headline: "Just Lost Your Job? Get a Clear 90-Day Plan."
- Description: "Free workbook + a complimentary planning session. No cost, no obligation."
- CTA button: Download

**Approved copy, A2**
- Intro text: "Severance decisions. COBRA vs. marketplace coverage. What to do with your old 401(k). These don't have to be solved this week, but they do need a plan. Checkpoint Planning built a free workbook specifically for people navigating a layoff."
- Headline: "A 90-Day Plan for Your Next Chapter"
- Description: "Free \"Your Next Checkpoint\" workbook. Fiduciary guidance, not a sales pitch."
- CTA button: Download

### Early Retirement
**Emotional truth**: excitement tangled with "did I actually do this
right?" A milestone that should feel like freedom but often feels
precarious.
**Direction**: forward-looking but grounded, not a stat card. A sense of
horizon, of a new chapter starting on solid footing. The 62-vs-70 Social
Security detail is real and useful information, worth keeping somewhere
in the design, but it shouldn't be the whole visual, it's the proof, not
the hook.

**Approved copy, A1**
Destination: `https://start.checkpointplanning.com/early-retirement.html?utm_source=linkedin&utm_medium=paid_social&utm_campaign=cp_earlyretirement_{yyyy-mm}&utm_content=li_a1`
- Intro text: "Retiring earlier than planned changes the math: Social Security timing, healthcare before Medicare, pension elections, and portfolio longevity. Before you commit to a date, get the free Early Retirement Checkpoint Guide and pressure-test the plan."
- Headline: "Retiring Early? Make Sure Your Money Can Too."
- Description: "Free guide + a complimentary session with a CRPC(TM) planner."
- CTA button: Download

**Approved copy, A2**
- Intro text: "Claiming Social Security at 62 instead of full retirement age can permanently cut your benefit by 25-30%. If your retirement timeline moved up, by choice or otherwise, this is the decision worth getting right before you file anything."
- Headline: "The Retirement Decisions That Don't Wait"
- Description: "Free Early Retirement Checkpoint Guide. No cost, no obligation session."
- CTA button: Download

### Divorce
**Emotional truth**: overwhelm plus a need for discretion and dignity.
This audience needs to feel safe and unjudged before anything else.
**Direction**: quiet, composed, private. No conflict imagery (hard
compliance rule). Avoid anything clinical or checklist-cold, the
current "checklist" visual reads more like an audit than support. A
single calm, protective visual detail (closed door, steady hands, soft
light) says more than a bulleted list.

**Approved copy, A1**
Destination: `https://start.checkpointplanning.com/divorce.html?utm_source=linkedin&utm_medium=paid_social&utm_campaign=cp_divorce_{yyyy-mm}&utm_content=li_a1`
- Intro text: "Divorce brings a wave of financial decisions on top of an already difficult time: settlement analysis, QDROs, tax filing status, rebuilding a budget on your own. A free guide on what to understand before you sign anything."
- Headline: "Financial Clarity Before You Sign a Settlement"
- Description: "Free Divorce Financial Checkpoint Guide. Confidential."
- CTA button: Download
- Note: small, capped test budget on LinkedIn, Facebook is the primary platform for this segment.

### Inheritance & Unexpected Wealth
**Emotional truth**: often grief tangled with responsibility, "I don't
want to mess this up" more than "what should I buy." Can carry guilt
about benefiting from a loss.
**Direction**: calm, unhurried, respectful, never celebratory or
wealth-flaunting, and never referencing loss/grief/funeral imagery
(hard compliance rule). The permission to slow down is the emotional
core, a visual that feels like a pause rather than a prompt to act.

**Approved copy, A1**
Destination: `https://start.checkpointplanning.com/inheritance.html?utm_source=linkedin&utm_medium=paid_social&utm_campaign=cp_inheritance_{yyyy-mm}&utm_content=li_a1`
- Intro text: "Received an inheritance? There's rarely a need to decide anything quickly. A free guide covering inherited IRA rules, tax basics, and the questions worth asking before you invest, spend, or sell."
- Headline: "Slow Down Before You Decide Anything"
- Description: "Free Inheritance Checkpoint Guide. No pressure, no obligation."
- CTA button: Download
- Note: small, capped test budget on LinkedIn, Facebook is the primary platform for this segment.

## The 12 carousel posts

Full approved caption text (title, body paragraphs, hashtags, and the
disclosure line) for all 12 posts lives in
`campaign/08-linkedin-content-calendar-month1.md`, that text is
locked and should be treated as the slide content to design around, not
rewritten. Quick reference for which posts need which emotional
treatment:

| # | Topic | Emotional core |
|---|---|---|
| 1 | Checkpoint Strategy, Phase 1: Where We Begin | Permission to not have it figured out yet |
| 2 | Job Loss: the first 30 days | Relief, "you don't have to solve everything this week" |
| 3 | What "fiduciary" actually means | Trust, transparency |
| 4 | Checkpoint Strategy, Phase 2: Identify and Protect | Stability before ambition |
| 5 | Early Retirement: 62 vs. 70 | Empowerment through informed choice |
| 6 | Personal story, endurance racing | Authenticity, the human behind the practice (photo-led) |
| 7 | Checkpoint Strategy, Phase 3: Plot Checkpoints | Progress made visible, momentum |
| 8 | Divorce: real value of a settlement | Protection, not being taken advantage of |
| 9 | Direct access differentiator | Being truly seen/known, not processed |
| 10 | Checkpoint Strategy, Phase 4 & 5: Implement, Track, Reset | Follow-through, a plan that adapts with you |
| 11 | Inheritance: step-up in cost basis | Permission to slow down |
| 12 | Month-end recap | Continuity, "one checkpoint at a time" as an identity, not a slogan |

Posts 6 and 9 are the two built around Scott directly and are the
strongest candidates for real photography over any graphic treatment,
these are where "authentic and human" has the most room to work.

## What's available to build from

- `website/assets/scott-marcoe.jpg`, current headshot.
- `website/assets/checkpoint-logo-mark.png`,
  `website/assets/checkpoint-logo-full.png`, logo files.
- Full approved copy for all posts and ads (see above and the source
  markdown files).
- Current v1 creative for reference (what's functional, what to improve
  on): `campaign/assets/ad-creatives/`, `campaign/assets/post-carousels/`.

## Sending finished creative back

Same file names as listed above, dropped into
`campaign/assets/ad-creatives/` (6 PNGs) and
`campaign/assets/post-carousels/` (12 PDFs, `post-01.pdf` through
`post-12.pdf`). That's all `campaign/tools/build_linkedin_month1_pdf.py`
needs to regenerate the compliance submission PDF around the new
creative without any other changes.
