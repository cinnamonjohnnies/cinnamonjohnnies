# Audience Targeting — By Platform, By Segment

Built around the platform constraints in `00-foundations.md` — Meta's
Special Ad Category rules out age/gender targeting for every segment
below; LinkedIn's professional-graph targeting is used where it has a real
signal to work with, and skipped where it doesn't.

Geography for all: **start national** (Scott serves clients across the
U.S. via video), but bias initial budget toward states with no state-level
barrier to a quick first meeting and where Checkpoint Planning already has
some presence — start with **California** as a weighted priority
(Orange County based, existing local trust/referral base) at roughly 2-3x
the bid/budget weight of the rest of the U.S., rather than excluding other
states outright.

---

## Job Loss & Layoff

**LinkedIn (primary platform for this segment)**
- Job change/company signals: target by **industries with recent/ongoing
  layoff activity** (tech, media, and other sectors currently in the news
  for reductions — review current layoff trackers monthly and adjust)
- Seniority: Manager through Director/VP (individual contributors and
  senior leaders both affected, but this range has the clearest ability
  to act on financial planning quickly)
- "Open to work" signal, where targetable, or recently changed job status
- Exclude: current Checkpoint Planning clients (build a suppression list
  once the CRM/client list is ready)

**Facebook/Instagram (secondary, broader reach)**
- Interests: career coaching, job search platforms, unemployment
  resources, severance/outplacement content
- Behavior: engaged with career-transition or job-search content recently
- Placement: feed + Stories; skip Audience Network initially (lower
  intent traffic, save it for a later optimization pass)

---

## Early Retirement

**LinkedIn (primary platform for this segment)**
- Seniority: Director, VP, C-level, or 15+ years tenure signals — proxies
  for someone in the pre-retirement window
- Industry: no strong restriction; broad white-collar/professional
  industries perform better for this segment than blue-collar
- Skills/groups: retirement planning, financial independence, "FIRE"
  movement groups where present
- Exclude: obviously early-career profiles (this is the one place
  seniority targeting does real work instead of age targeting, which
  isn't available on Meta and isn't the point on LinkedIn either)

**Facebook/Instagram (secondary)**
- Interests: retirement planning, Social Security, Medicare, 401(k)/IRA
  content, financial independence content
- Life-stage interest signals (empty nesters, grandparent-related
  interests) as a soft proxy — not age targeting, interest-based only
- Placement: feed-first; Instagram typically under-indexes for this
  segment, weight budget toward Facebook feed

---

## Divorce

**Facebook/Instagram (primary platform for this segment)**
- Interests: divorce support/recovery content, family law content people
  choose to follow, co-parenting resources
- Note: Meta previously offered detailed "relationship status: divorced"
  targeting and removed/restricted much of it under sensitive-category
  policy — don't plan around relationship-status targeting being
  available; build the audience from content-interest signals instead
- Broad geography, broad reach — this segment benefits more from message
  precision in the ad copy than from narrow targeting, given the platform
  constraint
- Placement: feed + Stories

**LinkedIn (secondary, low priority)**
- No professional-graph proxy for "going through a divorce" — if used at
  all, run as a low-budget test only, broad professional audience,
  and expect a higher cost per lead than Facebook for this segment

---

## Inheritance & Unexpected Wealth

**Facebook/Instagram (primary platform for this segment)**
- Interests: estate planning content, wills/trusts content, probate
  resources — people who've engaged with this content organically
- Life-stage interest signals: content related to loss of a family
  member (grief support pages, etc.) used carefully — see the tone note
  below, this is the most emotionally sensitive segment of the four
- Broad geography; this is a lower-volume, higher-value segment — expect
  smaller audience size and plan budget accordingly (see budget doc)

**LinkedIn (secondary, low priority)**
- Same logic as Divorce: no clean professional-graph proxy. Skip
  initially; revisit only if Facebook performance data suggests a
  wealthier/more professional sub-audience worth testing there directly

### A tone note specific to this segment

Inheritance often follows a death. Targeting interest signals tied to
grief or loss content should be used narrowly and the ad creative should
never reference the death itself — the ad copy in
`03-facebook-ads.md` leads with the financial-decision framing ("received
an inheritance"), never with loss framing. Platform ad review is also
stricter here; expect more review friction on this segment's ads than the
other three.

---

## Suppression list (build once available)

Before launching any segment, exclude:
- Existing Checkpoint Planning clients (upload as a Custom Audience
  exclusion on Meta; use a matched audience exclusion on LinkedIn)
- Anyone who submitted a lead form in the last 30 days for a *different*
  segment (avoid paying to re-target someone already in the pipeline)

This requires the client list and a recent-leads export — flag as a
to-do before the first campaign launches, not a blocker to building the
ads themselves.
