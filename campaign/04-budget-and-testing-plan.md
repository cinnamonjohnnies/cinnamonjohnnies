# Budget, Testing & Rollout Plan

This is the first paid campaign this funnel has ever run. The plan below
is built around validating the pipeline end-to-end before scaling spend,
not around launching all 8 segment/platform combinations at once.

Dollar figures below are **starting-point examples, not requirements** —
adjust to whatever total monthly budget is comfortable. The structure
(phasing, kill/scale rules) matters more than the specific numbers.

## Phase 1 — Validate the pipeline (Week 1-2)

Launch **one combination only**: Job Loss & Layoff on LinkedIn. This
segment/platform pairing is the strongest native fit (see
`01-audience-targeting.md`), and layoffs are a topical, easy-to-target
signal right now.

- Budget: ~$30-40/day (~$450-550 for the two weeks)
- Goal is not volume — it's confirming that a real ad click produces a
  real row in the Google Sheet with the right UTM data attached, that
  the landing page converts at a sane rate, and that ad review approves
  the creative without issues.
- Run both variants (A1/A2) at even budget split to get an early read on
  which hook performs, but don't make a final call yet — the sample size
  at this budget is too small to be confident.

**Do not proceed to Phase 2 until:**
- [ ] At least a handful of leads have landed correctly in the Sheet with
      accurate `utm_source` / `utm_campaign` / `utm_content`
- [ ] Cost per lead is in a sane range relative to the value of a client
      (see "What a lead is worth" below)
- [ ] No compliance or ad-review issues came up

## Phase 2 — Add the other 3 primary combos (Week 3-6)

Once Phase 1 validates the pipeline, add the other best-fit pairings:

- Early Retirement — LinkedIn
- Divorce — Facebook/Instagram
- Inheritance — Facebook/Instagram

- Budget: ~$25-35/day each (~$350-500/combo over 2 weeks)
- Same A/B structure (2 variants each) as Phase 1
- By the end of Phase 2 you have real cost-per-lead data across all 4
  segments on their strongest platform — this is the point where budget
  should start shifting toward whichever segment is actually converting,
  not staying evenly split by default

## Phase 3 — Fill in secondary combos + start reallocating (Week 7+)

Add the lower-priority pairings as small tests, not equal partners:

- Job Loss — Facebook (fills out the segment's reach beyond LinkedIn)
- Early Retirement — Facebook
- Divorce — LinkedIn (small capped test, e.g. $10-15/day — see the
  low-priority note in `02-linkedin-ads.md`)
- Inheritance — LinkedIn (same, small capped test)

From here on, this becomes an ongoing reallocation exercise: pull budget
from underperforming combinations, add it to whichever segment/platform
has the best cost per **booked Where We Begin session** (not just cost
per lead — a cheap lead that never books a session is worth less than a
pricier one that does).

## What a lead is worth (sizing the budget)

Checkpoint Planning's flat-fee packages run $1,200-$4,800, plus ongoing
AUM management on top for clients who use it. Even a conservative
estimate of client lifetime value comfortably supports a cost-per-lead in
the tens of dollars and a cost-per-booked-session in the low hundreds —
but there's no real benchmark yet for this specific funnel, which is
exactly why Phase 1 exists. Don't set a hard cost-per-lead target before
Phase 1 data exists; use Phase 1 to establish the baseline, then judge
Phase 2+ against it.

## Kill / scale rules (keep this simple)

- **Pause a variant** once it has spent ~$150-200 with zero leads, or a
  click-through rate meaningfully below the other variant in the same
  ad set (Meta and LinkedIn both show this in-platform — no need for
  external analysis).
- **Scale a variant** by increasing daily budget in modest increments
  (20-30% at a time) rather than large jumps — both platforms' delivery
  algorithms reset learning on big budget swings.
- **Reallocate across segments monthly**, not daily — weekly noise in a
  small-budget campaign is normal; judge segment performance on a
  rolling 2-4 week window using the Sheet's `Transition Type` and
  `UTM Campaign` columns.

## Weekly cadence

1. Pull the week's rows from the Google Sheet, grouped by
   `UTM Campaign` and `UTM Content`.
2. Note leads per combo, and mark in the `Status` column which ones
   converted to a booked Where We Begin session (this is the metric that
   actually matters — see above).
3. Compare against in-platform spend for the same date range on
   LinkedIn Campaign Manager and Meta Ads Manager.
4. Apply the kill/scale rules above before the next week's spend goes out.

A lightweight weekly cost-per-lead and cost-per-booking tracker (one row
per week, per combo) is worth setting up in a second tab of the same
Sheet once real data starts coming in — happy to build that when you're
ready for it.
