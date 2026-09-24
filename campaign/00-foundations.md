# Campaign Foundations: LinkedIn & Facebook

This is the base layer everything else in `campaign/` builds on: naming
convention, tracking, platform rules that shape targeting, and the order
this whole campaign gets built and launched in.

## Why this order

Ads are worthless if you can't tell which one produced a lead, and
targeting decisions are constrained by platform policy before they're a
matter of creative preference. So the build order is:

1. **Tracking** (already done, see below), every ad, on every platform,
   for every segment, needs a unique link so the Google Sheet tells you
   exactly which ad a lead came from, not just "Facebook" or "LinkedIn."
2. **Platform rules** (this doc), Meta in particular restricts financial
   services targeting in ways that change what's even possible to build.
   Know the constraint before writing a targeting plan around it.
3. **Audience targeting** (`01-audience-targeting.md`), who each ad is
   shown to, per platform, per transition.
4. **Ad copy** (`02-linkedin-ads.md`, `03-facebook-ads.md`), written to
   message-match each landing page's headline, so someone who clicks the
   ad sees the same promise on the page they land on.
5. **Budget & testing plan** (`04-budget-and-testing-plan.md`), how much,
   on what, and in what order the 4 segments x 2 platforms actually go live.
6. **Launch checklist** (`05-launch-checklist.md`), the pre-flight QA pass
   before any money is spent, including the compliance gate below.

## Compliance: read this before spending anything

**Paid social ads are marketing material under the same rules as the
website and lead magnets.** FINRA/Ameritas compliance review applies to ad
copy and creative, not just the landing pages they point to. Submit the ad
copy in `02-linkedin-ads.md` and `03-facebook-ads.md` for approval the same
way the website went through, before any campaign goes live, not after.
Character limits on both platforms make the full business-name/FINRA-SIPC
disclosure impossible to fit in ad copy itself; standard (and compliant)
practice is a short disclosure line in the ad plus the full disclosure on
the landing page it links to, which is already in place on every page.

## Tracking: UTM convention

Every ad link uses the same 4 parameters so the Sheet can answer "which
platform, which campaign, which specific ad" for every lead. The lead
capture forms and backend already read and store all four (see
`website/script.js`, `website/google-apps-script/Code.gs`), the Sheet's
header row needs two columns added once, per `docs/SETUP.md`.

```
utm_source   = linkedin | facebook
utm_medium   = paid_social
utm_campaign = cp_{segment}_{yyyy-mm}
utm_content  = {platform-short}_{variant-id}
```

**Segments** (matches the 4 landing pages): `jobloss`, `earlyretirement`,
`divorce`, `inheritance`

**Example full links** (build these in each platform's ad UI, or append by
hand):

```
https://checkpointplanning.com/job-loss.html
  ?utm_source=linkedin&utm_medium=paid_social
  &utm_campaign=cp_jobloss_2026-10&utm_content=li_a1

https://checkpointplanning.com/divorce.html
  ?utm_source=facebook&utm_medium=paid_social
  &utm_campaign=cp_divorce_2026-10&utm_content=fb_a2
```

`utm_content` variant IDs (`a1`, `a2`, `b1`...) map directly to the
lettered/numbered ad variants in `02-linkedin-ads.md` and
`03-facebook-ads.md`, keep that mapping when you build the ads so a
number in the Sheet always traces back to one specific headline/image
pairing.

## Platform rules that shape everything downstream

### Meta (Facebook/Instagram): Special Ad Category

Financial services ads on Meta fall under the **Special Ad Category for
Credit**. This isn't optional, Meta's system detects financial-services
content and applies it automatically. It measurably restricts targeting:

- **No age or gender targeting.** Every ad must be eligible to all adults
  18+ regardless of age or gender you might otherwise want to target.
- **No detailed demographic/interest exclusions** in the way standard ads
  allow (no excluding by income, homeownership, etc. as a targeting lever).
- **Geographic targeting is limited**: no pinpoint radius targeting around
  a specific address; targeting works at the ZIP/city/region level instead.
- **Custom Audiences and Lookalike Audiences** are more restricted than for
  standard ad campaigns (available, but built and used differently, plan
  for this when you're ready to build retargeting).

Practical effect: Meta targeting for this campaign leans on **broad
geography + interest/behavior signals + placement**, not narrow demographic
slicing. `01-audience-targeting.md` is written around this constraint, don't build a Facebook ad set that tries to exclude by age or gender, it
will be rejected or auto-corrected.

### LinkedIn: no equivalent restriction, but different strengths

LinkedIn does not have a Special Ad Category system like Meta's. Standard
professional-graph targeting (job title, seniority, industry, company size,
skills) is available. This makes LinkedIn the stronger platform for the two
segments with a clear professional signal, **Early Retirement** (title/
seniority/tenure proxies for someone approaching retirement) and, to a
lesser extent, **Job Loss & Layoff** (targeting by industry currently
undergoing layoffs, or "open to work" signals). It's a weaker fit for
**Divorce** and **Inheritance**, which have no professional-graph proxy, those two lean more heavily on Meta.

### Both platforms

- No health, legal, or financial "predatory" claims, no guaranteed
  outcomes, no implied inside knowledge, no urgency/fear-based language
  Meta or LinkedIn's ad review would flag as sensitive-category exploitation
  (both platforms specifically review financial-services ads for this).
- Landing page URL in every ad must match approved, compliance-cleared
  copy exactly, no last-minute page edits post-approval without informing
  compliance.

## Segment -> platform fit (at a glance)

| Segment | LinkedIn fit | Facebook/Instagram fit |
|---|---|---|
| Job Loss & Layoff | Strong (industry/title targeting) | Strong (broad reach, life-stage interest signals) |
| Early Retirement | Strong (seniority/tenure targeting) | Moderate (age-neutral targeting is the constraint) |
| Divorce | Weak (no professional-graph proxy) | Strong (best-fit platform for this segment) |
| Inheritance | Weak (no professional-graph proxy) | Moderate (harder to target directly; interest-based) |

This drives the launch order in `04-budget-and-testing-plan.md`: start
where platform fit is strongest for each segment, rather than launching
all 8 combinations at once.
