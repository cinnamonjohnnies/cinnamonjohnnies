# Building the LinkedIn Page and Growing Followers

Follows on from Step 0 in `06-linkedin-launch-today.md` (creating the
Page itself). This covers finishing the Page so it looks credible to
anyone who clicks through from an ad, then growing real followers, then
keeping it active over time. None of this blocks the ad campaign, a
brand-new Page with zero followers can run Sponsored Content
immediately, but a page that looks alive matters once real traffic
starts landing on it.

## Priority order for today

1. Paste in the About section and Specialties below (10 minutes).
2. Add a banner image and pin one Featured link (10 minutes).
3. ~~Invite your personal LinkedIn connections to follow the Page~~,
   done, 259 invites sent.
4. Submit the first post (below) to compliance, then publish it once
   cleared, so the Page isn't empty while those invites are being
   reviewed. Ask two or three trusted contacts to engage with it in the
   first hour.
5. Everything else in this doc (content cadence, ongoing growth) is a
   next-few-weeks project, not a today project.

## Complete the Page

**About / Overview** (paste into the Page's About section, LinkedIn
allows up to 2,000 characters, this comes in under that):

> Checkpoint Planning helps people navigate major life and career
> transitions, job loss, divorce, early retirement, and inheritance,
> with a structured, fiduciary planning process.
>
> Founded by Scott Marcoe, CRPC (TM), Checkpoint Planning brings clarity
> to the moments when financial decisions are most consequential and
> most often made without a plan. The Checkpoint Strategy (TM), a
> five-phase framework built from Scott's background as a competitive
> endurance athlete, breaks big financial questions into manageable
> steps: Where We Begin, Identify and Protect, Plot Checkpoints,
> Implement, and Track and Reset.
>
> As a fiduciary, Scott is legally required to act in your best
> interest at all times. Every client works directly with him, in every
> meeting, every review, every conversation.
>
> The best next step is a conversation. The Where We Begin session is
> complimentary and carries no obligation.
>
> Scott Marcoe offers products and services using the following
> business names: Checkpoint Planning, Capstone Financial Group,
> insurance and financial services. Ameritas Investment Company, LLC
> (AIC), Member FINRA/SIPC, securities and investments. Ameritas
> Advisory Services, LLC (AAS), investment advisory services. AIC and
> AAS are not affiliated with Capstone Financial Group.

**Specialties** (LinkedIn's tag-style field, add as many as fit):
Financial Planning, Retirement Planning, Divorce Financial Planning,
Life Transition Planning, Career Transition Planning, Estate Planning
Coordination, Fiduciary Financial Advisor, Wealth Management, Tax
Planning Coordination, Insurance Planning

**Website:** `https://checkpointplanning.com`

**Banner image:** built and ready at `website/assets/linkedin-banner.png`
(1128x191, LinkedIn's exact Page banner size), the site's hero gradient
with the wordmark, tagline, and a small dotted-path motif echoing the
logo. Upload it as-is under the Page's banner image setting. Source is
`campaign/assets/linkedin-banner/banner.html`, rerun
`campaign/assets/linkedin-banner/render.py` if the copy or colors ever
need to change. Don't leave the default LinkedIn gray banner in the
meantime, it's the single biggest giveaway of an unfinished Page.

**Featured section:** pin a link to the "Where We Begin" session
(`contact.html`) as the primary Featured item. This is the same page the
ads point to, so it doubles as a preview for anyone browsing the Page
directly instead of clicking an ad.

## First post: introduction

Publish this before the invited connections start checking the Page out,
an empty feed under an empty banner undoes a lot of the credibility work
above. Written to reuse already-approved website language (About page,
bio, tagline) so it should clear compliance quickly, same reasoning as
the ad copy: **still submit it before publishing, don't skip that step
just because it's a low-risk introduction post.**

**Post image:** `website/assets/linkedin-post-image-01.png` (1200x1200,
square), same design system as the banner. Source is
`campaign/assets/linkedin-post-image-01/postcard.html`, rerun
`campaign/assets/linkedin-post-image-01/render.py` to regenerate after
edits.

**Post copy** (paste as-is, or adjust in your own voice, the structure
and disclosure line matter more than the exact wording):

> Financial decisions rarely wait for a good time to show up.
>
> A layoff. A divorce. An unexpected inheritance. Retiring earlier than
> planned. These are the moments when the stakes are highest, and a plan
> is usually missing entirely.
>
> I started Checkpoint Planning to change that.
>
> My approach is built around The Checkpoint Strategy, a five-phase
> framework I developed after years of competitive endurance racing
> (state champion mountain biking, national champion in 24-hour racing).
> Winning those races never came from one big push. It came from
> breaking an enormous challenge into manageable checkpoints and
> adjusting to real conditions along the way.
>
> Financial transitions work the same way.
>
> As a fiduciary and CRPC, I work directly with every client. No
> hand-offs, no product quotas, just a structured process built for the
> moment you're actually in.
>
> If you or someone you know is navigating a major life transition, I'd
> love to connect. The first conversation, called Where We Begin, is
> complimentary and carries no obligation. Link in the comments.
>
> #FinancialPlanning #FiduciaryAdvisor #LifeTransitions #RetirementPlanning #DivorceFinancialPlanning
>
> Scott Marcoe offers products and services using the following business
> names: Checkpoint Planning, Capstone Financial Group, insurance and
> financial services. Ameritas Investment Company, LLC (AIC), Member
> FINRA/SIPC, securities and investments. Ameritas Advisory Services, LLC
> (AAS), investment advisory services. AIC and AAS are not affiliated
> with Capstone Financial Group.

**Put the link in the first comment, not the post body.** LinkedIn's
algorithm measurably suppresses reach on posts containing an outbound
link; posting the link as the first comment (right after publishing,
from your own account) avoids that penalty while still getting people to
the Where We Begin page. Comment something like: "Here's where to start
a conversation: [contact.html link]".

**Ask two or three trusted contacts to like or comment within the first
hour.** Early engagement velocity is what LinkedIn's algorithm uses to
decide how far to push a post; a post that sits at zero engagement for
hours gets shown to fewer people than one that picks up a few
interactions right away. A text to two or three people (a past colleague,
someone from the AISS board, a referral-partner contact) asking them to
take a look costs nothing and meaningfully changes the post's reach.

## Making the Page look legitimate, beyond the basics

A handful of details separate a Page that looks like a real, active
practice from one that looks freshly created for an ad campaign:

- **Link your personal profile to the Page.** On your personal LinkedIn
  profile, add "Founder, Checkpoint Planning" (or similar) as your
  current position under Experience, and set the Company field to the
  actual Checkpoint Planning Page rather than free text. This makes
  LinkedIn show "Scott Marcoe works here" on the Page itself, and is one
  of the strongest legitimacy signals a small Page can have, it's the
  difference between a Page that's clearly tied to a real person and one
  that exists in isolation.
- **Fill in the Locations field** with the Irvine office address (3333
  Michelson Drive, Irvine, CA 92612). Pages with a real address read as
  more established than ones with only a website link.
- **Claim a clean custom URL** if you haven't already
  (`linkedin.com/company/checkpoint-planning` or the closest available
  variant), a default numeric URL is another small tell.
- **Respond to every comment on the first post within a few hours**,
  especially in the first days while the 259 invited connections are
  actively checking the Page out. A Page that replies quickly looks
  managed; one that doesn't looks abandoned.
- **Publish a second post within the first week**, doesn't need to be
  elaborate, one of the content pillars below works fine. A single post
  followed by weeks of silence reads worse than no post at all once
  someone scrolls the Page's activity.
- **Optional, lower priority: LinkedIn Page verification.** LinkedIn
  offers a verified badge for Pages through Microsoft Entra Verified ID.
  It's not required to run ads or look credible at this stage, worth
  revisiting once the Page has some real activity behind it, not before.

## Getting your first followers (zero to a real audience)

**You've already done the highest-leverage single action**, inviting
your personal network. Once those 259 invites convert to follows over
the next several days, the tactics below keep the momentum going rather
than starting from scratch.

Your existing network already includes exactly the kind of people worth
having as followers: past colleagues, the AISS board and STEM Scholars
community, the endurance racing/mountain biking community, and any of
the referral-partner contacts named in
`prospecting/referral-partner-strategy.md` (divorce attorneys, CPAs,
estate attorneys) who are already connections.

**Add the Page everywhere your brand already shows up:**
- Email signature (a simple "Follow Checkpoint Planning on LinkedIn"
  link)
- Website footer, worth a small addition alongside the existing contact
  links (say the word and I'll add it to all 10 pages)
- The "Where We Begin" confirmation and any future email sequence
  footers, once those go through compliance

**Engage before you ask.** Commenting thoughtfully on posts from
existing connections, especially the referral-partner types (divorce
attorneys, CPAs, HR/outplacement contacts), builds visibility with
exactly the audience worth having, often before they even notice the
Page exists. This costs time, not budget, and compounds.

**Paid ads themselves add followers as a side effect**, but don't rely
on this alone; someone has to click through to the Page specifically to
follow it, most ad clicks go straight to the landing page instead.

## Ongoing content: cadence and pillars

Two to three posts a week is a realistic, sustainable starting cadence
for a solo practice. Content pillars, rotate through these rather than
posting only promotional material:

1. **Transition education** (the bulk of it), a short, standalone tip
   from one of the four lead magnets or landing pages, rewritten for a
   LinkedIn post rather than copy-pasted. Example: one post could cover
   just the "step-up in cost basis" point from the Inheritance guide.
2. **The Checkpoint Strategy framework itself**, explaining one phase at
   a time (Where We Begin, Identify and Protect, etc.) as its own post.
3. **Scott's personal story**, the endurance-athlete-to-financial-planner
   throughline is a genuine differentiator and performs well as
   occasional personal content, not every post, but regularly.
4. **Fiduciary/practice differentiators**, short posts on what fee-only,
   fiduciary, no-commission-on-managed-assets actually means for a
   client, in plain language.

Avoid: specific client stories or testimonials (compliance and privacy
issue), performance claims, anything that reads as investment advice
rather than education.

## Compliance workflow for ongoing posts

Every organic post is public marketing material under the same rules as
the website and ads, technically it needs review too. Submitting each
post individually isn't practical for a 2-3x/week cadence, so batch it:
draft 2-4 weeks of posts at once, submit the batch to Ameritas
compliance together, then schedule them out once approved (LinkedIn's
native scheduler, or a tool like Buffer/Hootsuite if managing multiple
weeks at a time gets unwieldy). Treat this the same way the ad copy and
lead magnets were batched for review, one clean submission beats a
trickle of one-offs.
