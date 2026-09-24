# Pre-Launch Checklist

Run through this in order before the Phase 1 campaign (Job Loss &
Layoff, LinkedIn, per `04-budget-and-testing-plan.md`) goes live, and
again before each new segment/platform combo launches in Phase 2/3.

## 1. Compliance gate (blocking, do not skip)

- [ ] Ad copy for this segment/platform (from `02-linkedin-ads.md` or
      `03-facebook-ads.md`) has been submitted to and approved by
      Ameritas compliance, the same as the website and lead magnets were
- [ ] Any compliance-requested edits have been made to the copy in this
      repo before the ad is built in-platform, so the live ad matches
      what was approved exactly

## 2. Site & tracking readiness

- [ ] The site is live at `checkpointplanning.com` and the specific
      landing page for this segment loads correctly
- [ ] `LEAD_WEBHOOK_URL` in `website/script.js` is set to the real Apps
      Script deployment URL (not the placeholder), see `docs/SETUP.md`
- [ ] The Google Sheet header row includes **UTM Medium** and
      **UTM Content** columns (added per `docs/SETUP.md`), confirm
      before launch, since ad-level attribution depends on it
- [ ] Test the full path once, manually: open the landing page with a
      test UTM string appended (use `utm_content=test`), submit the
      form with a real (or clearly marked test) entry, and confirm the
      row appears in the Sheet with every UTM field populated correctly
- [ ] Delete or clearly mark the test row once confirmed

## 3. Platform account setup

**LinkedIn Campaign Manager**
- [ ] Campaign Manager account connected to Checkpoint Planning's
      LinkedIn Page
- [ ] Payment method added
- [ ] Insight Tag already sits in every page's `<head>`; replace
      `REPLACE_WITH_YOUR_LINKEDIN_PARTNER_ID` with your real Partner ID
      (from Campaign Manager > Account Assets > Insight Tag) across all
      10 HTML files, then redeploy. See `06-linkedin-launch-today.md`
      Step 1 for the walkthrough.
- [ ] Conversion ID created in Campaign Manager (type: Lead, tracking
      method: Insight Tag, not a URL rule, since the form doesn't
      navigate to a new page) and pasted into `LINKEDIN_CONVERSION_ID`
      in `website/script.js`, then redeployed
- [ ] Campaign objective set to **Website Conversions** (or Lead
      Generation only if you specifically want native LinkedIn lead
      forms instead of driving to the landing page, default
      recommendation is Website Conversions, since it sends traffic to
      the real landing page with its full disclosures already in place)

**Meta Ads Manager**
- [ ] Ads Manager account connected to a Facebook Page (and Instagram
      account, if running Instagram placements)
- [ ] Payment method added
- [ ] Meta Pixel installed on the site (same rationale as the LinkedIn
      Insight Tag, install site-wide)
- [ ] Confirm the ad account shows **Special Ad Category: Credit**
      selected for this campaign (Meta may prompt for this automatically
      given the content, don't override it)
- [ ] Campaign objective set to **Leads** or **Traffic** pointed at the
      landing page URL with full UTM parameters attached

## 4. Ad build QA

- [ ] Destination URL on every ad matches the exact format in
      `00-foundations.md`, with the correct segment, platform, campaign
      month, and content variant ID
- [ ] Headline, primary/intro text, and description match the
      compliance-approved copy exactly, no live edits in-platform
- [ ] CTA button matches what's specified in the ad copy doc
- [ ] Creative/image matches the concept notes (or the
      compliance-approved final creative, once produced)
- [ ] Click the ad preview's destination link before publishing and
      confirm it lands on the correct page with UTM parameters intact

## 5. Go live

- [ ] Set the daily budget per `04-budget-and-testing-plan.md` for
      whichever phase you're in
- [ ] Note the launch date/time somewhere trackable (a note in the
      Sheet's second tab, or wherever the weekly tracker ends up living)
- [ ] Calendar reminder for the Phase 1 checkpoint (end of week 2) to
      review the "do not proceed to Phase 2 until" criteria in
      `04-budget-and-testing-plan.md`
