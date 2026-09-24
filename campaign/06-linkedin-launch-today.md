# LinkedIn Launch: Today's Build

This is the concrete, do-this-now version of the plan in
`00-foundations.md` through `05-launch-checklist.md`, narrowed to exactly
what to do today. It follows Phase 1 from `04-budget-and-testing-plan.md`:
one segment, one platform, small budget, built to validate the pipeline
before anything scales.

**Segment: Job Loss & Layoff. Platform: LinkedIn.** This pairing has the
strongest native fit of the four segments (see `01-audience-targeting.md`)
and is the fastest to stand up cleanly today.

## Where things stand right now

- A LinkedIn Company Page for Checkpoint Planning needs to exist before
  anything else here works, Sponsored Content ads require one and a
  personal profile can't run them. See Step 0 if that Page doesn't
  exist yet.
- The website went to Ameritas compliance and is pending approval; no
  issues are expected, it's a matter of timing.
- **The ad copy in `02-linkedin-ads.md` has not been separately submitted
  for compliance review.** It's new content, written after the website
  went in. Build the campaign today, but leave it paused (LinkedIn lets
  you build a fully configured campaign in Draft status without spending
  anything) until that copy clears review. Submitting it should be fast
  since it reuses approved website language and disclosures, but don't
  skip the step.
- Tracking infrastructure was extended today specifically for this
  launch: the LinkedIn Insight Tag is now on every page (`<head>`, all 10
  pages), and a real conversion event fires in `website/script.js` on a
  successful form submission. Two placeholder IDs need to be filled in
  before anything will actually track, see Step 1 below.

## Step 0: Set up a LinkedIn Company Page

LinkedIn Sponsored Content, the ad format this whole plan is built
around, can only run through a **Company Page**. A personal profile,
even one built and used for the business, cannot be the identity behind
a Sponsored Content ad; Campaign Manager requires a Page to attach the
campaign to. This is a one-time setup, not a recurring step.

1. Log into your existing personal LinkedIn profile (no new personal
   account needed, this stays as-is).
2. Click the **For Business** icon (grid icon, top right), scroll to
   **Create a Company Page**, or go directly to
   `linkedin.com/company/setup/new/`.
3. Choose **Small business** as the Page type (the other options,
   Medium/Large business, Showcase Page, Educational institution, don't
   fit a solo practice).
4. Fill in the required fields:
   - **Page name:** Checkpoint Planning
   - **LinkedIn public URL:** claim `linkedin.com/company/checkpoint-planning`
     if available, otherwise the closest variant
   - **Website:** `https://checkpointplanning.com`
   - **Industry:** Financial Services (or Financial Planning, if offered
     as a more specific option)
   - **Company size:** 1-10 employees, or Self-employed
   - **Company type:** Self-employed or Privately Held
   - **Logo:** use `website/assets/checkpoint-logo-mark.png` (the square
     icon mark reproduces better at LinkedIn's small logo size than the
     full wordmark)
   - **Tagline:** "Financial Clarity for Life's In-Betweens", already the
     site's tagline, keep it consistent
5. Check the box confirming you're authorized to act on the
   organization's behalf, then **Create page**. You're automatically
   the Page's Super Admin.
6. Fill out the **About** section before running any ads against it,
   since curious clickers will visit the Page itself. Include the same
   disclosure language used in the site footer (business names, FINRA/
   SIPC, not affiliated with Capstone Financial Group). This is public
   marketing material too, worth a quick compliance glance alongside the
   ad copy in Step 5, even though it's lower-risk than the ads
   themselves.
7. Add a cover image and at least one post (even just introducing the
   practice) so the Page doesn't look empty when someone clicks through
   from an ad out of curiosity.
8. Back in [LinkedIn Campaign Manager](https://www.linkedin.com/campaignmanager/),
   when you create the ad account (or edit an existing one), set this
   new Page as the account's **associated Page**. This is what makes
   Sponsored Content available as a format, everything in Step 3 below
   depends on this being set.

No minimum follower count or waiting period is required before running
ads from a brand-new Page.

## Step 1: Fill in the two LinkedIn IDs (do this first)

Everything else depends on these. Both come from LinkedIn Campaign
Manager, and you'll get the first one before you even build the campaign.

1. Go to [LinkedIn Campaign Manager](https://www.linkedin.com/campaignmanager/),
   create or select the Checkpoint Planning ad account.
2. Under **Account Assets, Insight Tag**, copy your **Partner ID** (a
   short number). Find and replace **every occurrence** of
   `REPLACE_WITH_YOUR_LINKEDIN_PARTNER_ID` across all 10 HTML files in
   `website/` with that number (it appears twice per page, once in the
   script block, once in the `<noscript>` fallback).
3. Deploy/redeploy the site with that change before moving on. The
   Insight Tag needs to be live before LinkedIn will show it as
   "Active" in Campaign Manager, usually within a day of real traffic.
4. You won't have a **Conversion ID** yet, that gets created in Step 3
   below, once the campaign objective is set. Come back and fill
   `LINKEDIN_CONVERSION_ID` in `website/script.js` at that point, then
   redeploy again.

## Step 2: Confirm the lead form itself is live

Before spending a dollar on traffic, confirm a submitted form actually
produces a lead. Do this once, today, if it hasn't been done since the
last content changes:

1. Follow `docs/SETUP.md` to deploy `website/google-apps-script/Code.gs`
   and get the real `LEAD_WEBHOOK_URL` into `website/script.js` (skip if
   already done).
2. Add the two missing columns (**UTM Medium**, **UTM Content**) to the
   Google Sheet header row, between "UTM Campaign" and "Status", if not
   already added.
3. Open `job-loss.html` on the live site with a test query string:
   `?utm_source=linkedin&utm_medium=paid_social&utm_campaign=cp_jobloss_test&utm_content=test`
4. Submit the form with a clearly marked test entry (e.g. name "TEST").
   Confirm a row appears in the Sheet with every UTM field populated.
5. Delete that test row once confirmed.

## Step 3: Build the campaign in LinkedIn Campaign Manager

Build this as a new **Campaign Group** called `Checkpoint Planning` (if
one doesn't exist yet), with a single campaign inside it.

**Campaign settings**

| Field | Value |
|---|---|
| Campaign name | `cp_jobloss_{current-month}_linkedin` (e.g. `cp_jobloss_2026-09_linkedin`) |
| Objective | **Website conversions** (this is where you'll create the Conversion ID, see below) |
| Format | Single image ad |
| Audience location | United States, with a manual bid weight toward California if your bidding tool allows it (see `01-audience-targeting.md`); otherwise leave broadly national for now and revisit once Phase 1 data exists |
| Audience attributes | Job Experience > Industry: target industries currently seeing layoffs (check a current layoff tracker before finalizing the list, this changes month to month); Job Experience > Seniority: Manager through Director/VP |
| Audience expansion | Off (keep targeting tight for this first, small-budget test) |
| Budget | Daily budget $30 to $40, no end date needed but plan to review at the Week 2 mark |
| Bid strategy | Maximum delivery (automated), simplest option for a first test |
| Ad rotation | Even, run both variants (A1/A2) at equal weight |

**Creating the Conversion ID (part of setting the objective):**
When you select "Website conversions," LinkedIn prompts you to create a
conversion action. Create one named `Lead: Job Loss Landing Page`, type
**Lead**, tracking method **Insight Tag** (not a URL rule, since the form
doesn't navigate to a new page). LinkedIn will show you the Conversion ID
for this action, put that into `LINKEDIN_CONVERSION_ID` in
`website/script.js`, and redeploy the site.

## Step 4: Build the two ads

Use Variant A1 and A2 from `02-linkedin-ads.md` exactly as written
(pending the compliance check in Step 5, don't launch before that clears).
Destination URLs, with the current month filled in:

```
Variant A1:
https://checkpointplanning.com/job-loss.html?utm_source=linkedin&utm_medium=paid_social&utm_campaign=cp_jobloss_{current-month}&utm_content=li_a1

Variant A2:
https://checkpointplanning.com/job-loss.html?utm_source=linkedin&utm_medium=paid_social&utm_campaign=cp_jobloss_{current-month}&utm_content=li_a2
```

Paste in the intro text, headline, and description exactly as written in
`02-linkedin-ads.md`. Leave the image as a placeholder or a simple
brand-colored graphic for now if final creative isn't ready, a plain
on-brand graphic beats delaying the whole build. Set the CTA button to
**Download** on both.

## Step 5: Compliance, then go live

1. Submit the two ad variants (exact text as built in Campaign Manager)
   to Ameritas compliance today, alongside or right after the website
   package. Reference that it reuses approved website copy and
   disclosures.
2. Leave the campaign in **Draft** (LinkedIn's term for a built-but-not-
   submitted campaign) until approval comes back. Building it today does
   not mean spending today.
3. Once approved: submit the campaign for LinkedIn's own ad review
   (separate from compliance, this is LinkedIn checking the ad meets
   their platform policies, usually resolves within 24 hours), then
   activate.

## Step 6: What to check over the next two weeks

This is Phase 1 from `04-budget-and-testing-plan.md`. Don't add more
segments or platforms until these are true:

- [ ] Leads are landing in the Google Sheet with correct
      `utm_source` / `utm_campaign` / `utm_content` values matching the
      variant that was actually clicked
- [ ] LinkedIn Campaign Manager shows the Conversion Tracking action
      firing (visible under the campaign's results once a few conversions
      have happened)
- [ ] Cost per lead is in a sane range (see "What a lead is worth" in
      `04-budget-and-testing-plan.md`)
- [ ] No compliance or LinkedIn ad-review issues came up

Once those hold, move to Phase 2: Early Retirement on LinkedIn, and
Divorce plus Inheritance on Facebook, per `04-budget-and-testing-plan.md`.
