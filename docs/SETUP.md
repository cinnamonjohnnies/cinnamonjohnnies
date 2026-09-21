# Checkpoint Planning, Lead Generation System: Setup Guide

This repo contains a complete lead-generation system built from your existing
Checkpoint Planning collateral (Intro Presentation, Menu of Services, Checkpoint
Strategy, Fees & Services, your bio, and the "Your Next Checkpoint" workbook).

## What's included

```
website/                    Static site (HTML/CSS/JS, no build step)
  index.html                 Homepage
  about.html                  About Scott + coordinated support areas
  services.html                Full services menu + links to transition pages
  process.html                 The Checkpoint Strategy + Working Together timeline
  fees.html                    Planning packages + AUM fee schedule
  contact.html                  Contact form + full FAQ + map
  job-loss.html               Job Loss & Layoff landing page
  early-retirement.html       Early Retirement landing page
  divorce.html                 Divorce landing page
  inheritance.html            Inheritance & Unexpected Wealth landing page
  styles.css                   Shared brand styles
  script.js                    Lead form handling (posts to Google Sheets)
  assets/                       Your real logo, icon mark, CRPC badge, and headshot
  google-apps-script/Code.gs   Backend script that writes form leads to Google Sheets

lead-magnets/                Downloadable guides used as opt-in incentives
  your-next-checkpoint-job-loss-workbook.pdf   (your existing workbook, reused)
  early-retirement-checkpoint-guide.md
  divorce-financial-checkpoint-guide.md
  inheritance-checkpoint-guide.md

email-nurture/               5-email nurture sequences, one per transition
  job-loss-sequence.md
  early-retirement-sequence.md
  divorce-sequence.md
  inheritance-sequence.md

prospecting/                 Outbound / referral-partner strategy
  referral-partner-strategy.md
```

## 1. Connect the lead form to your Google Sheet

A Google Sheet called **"Checkpoint Planning - Website Leads"** has already
been created in your Google Drive with the right columns
(Timestamp, Name, Email, Phone, Transition Type, Source Page, Message, Lead
Magnet Downloaded, UTM Source, UTM Campaign, Status).

**Before running any paid campaigns**, insert two more columns into that
header row, between "UTM Campaign" and "Status": **UTM Medium** and
**UTM Content**. The forms and `Code.gs` already send this data (added to
support per-ad attribution for the LinkedIn/Facebook campaign, see
`campaign/00-foundations.md`); the Sheet's header row just needs to catch up
since there's no API used here that can edit a single cell for you.

To connect the website forms to it:

1. Open the Sheet, go to **Extensions → Apps Script**.
2. Delete any placeholder code and paste in the contents of
   `website/google-apps-script/Code.gs`.
3. Click **Deploy → New deployment**.
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Click **Deploy**, authorize the permissions Google asks for (it needs to
   write to the Sheet and, optionally, send email).
5. Copy the resulting **Web app URL** (ends in `/exec`).
6. Open `website/script.js` and replace:
   ```js
   const LEAD_WEBHOOK_URL = "REPLACE_WITH_YOUR_APPS_SCRIPT_WEB_APP_URL";
   ```
   with your actual URL.
7. Re-deploy the site (see step 2 below).

Every form submission across all five pages will now append a row to the
Sheet and, if you keep the `NOTIFY_EMAIL` line in `Code.gs`, email you
immediately.

> If you'd rather use a different destination (a CRM, Mailchimp/ActiveCampaign,
> a Zapier webhook), swap the `fetch()` call in `script.js`, the honeypot
> spam trap and UTM capture will keep working as-is.

## 2. Host the site

This is a static site, no server or database required beyond the Apps
Script webhook above. Easiest options:

- **Netlify / Vercel (recommended):** drag-and-drop the `website/` folder,
  or connect this GitHub repo and set the publish directory to `website/`.
- **GitHub Pages:** enable Pages on this repo, pointed at the `website/`
  folder (or a `gh-pages` branch containing its contents).

Once hosted, point `checkpointplanning.com` (or a subdomain like
`start.checkpointplanning.com` for campaign tracking) at it via your
domain registrar's DNS settings.

## 3. Wire up analytics and campaign tracking

Every landing page reads `utm_source` and `utm_campaign` from the URL and
logs them with the lead. Use links like:

```
https://checkpointplanning.com/job-loss.html?utm_source=linkedin&utm_campaign=layoff_q1
```

If you use Google Analytics or Google Tag Manager, add your tracking
snippet to the `<head>` of each HTML file, `script.js` already pushes a
`lead_form_submit` event to `window.dataLayer` on every successful
submission if GTM is present.

## 4. Turn the three new guides into designed PDFs

`early-retirement-checkpoint-guide.md`, `divorce-financial-checkpoint-guide.md`,
and `inheritance-checkpoint-guide.md` are written to match the structure and
tone of your existing "Your Next Checkpoint" workbook. Hand these to
whoever designed the original workbook (or use the same template) to
produce matching branded PDFs, then update the corresponding
`lead_magnet` value and download link on each landing page.

## 5. Compliance review: do this before going live

Because Checkpoint Planning operates under Ameritas Investment Company /
Ameritas Advisory Services (FINRA/SIPC), **all new marketing
material, the landing pages, the three new lead magnets, and the five
email sequences, should go through your normal broker-dealer/RIA
compliance review and approval process before publishing**, the same way
your existing Intro Presentation and workbook were presumably reviewed.
Pay particular attention to:

- The required-disclosure footer (already included on every page and
  guide, matching your existing materials)
- Any performance, return, or "guarantee" language (none was used, but
  re-check before publishing)
- State registration: confirm you're licensed/registered to solicit
  clients in any state you specifically target with paid ads

## 6. Set up the email sequences

The five-email sequences in `email-nurture/` are written as
send-ready copy with `{{first_name}}` merge tags, meant to be loaded into
whatever ESP/CRM you use (Mailchimp, ActiveCampaign, HubSpot, etc.),
triggered by the matching lead magnet download. Each sequence spans
roughly two weeks (Day 0, 2, 5, 9, 14) and ends by moving non-responders
to a general newsletter list rather than continuing indefinitely.

## 7. Referral-partner prospecting

See `prospecting/referral-partner-strategy.md` for the full rationale and
approach. In short: rather than cold-contacting individuals based on
scraped personal-transition data (a compliance and trust risk), the
outbound motion targets **referral partners**, divorce attorneys, estate
attorneys, CPAs, and outplacement firms in Orange County, using Clay or
Vibe Prospecting to build and enrich a target list. Ask me to run a live
sample pull whenever you're ready; those tools consume paid credits per
enriched contact, so I held off running one without your go-ahead.

## Quick local preview

No build step is required. From the `website/` folder, either open
`index.html` directly in a browser, or run a tiny local server so the
relative links behave exactly like production:

```
cd website
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.
