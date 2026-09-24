# Deploying to checkpointplanning.com

The site is live at `checkpointplanning.com` (the root domain, not the
`start.` subdomain, that plan was dropped). It's fully static, any host
that serves plain files works.

The site includes the full "base" site (Home, About, Services, Our
Process, Fees, Contact) plus the four transition landing pages (Job
Loss, Early Retirement, Divorce, Inheritance), all matching the
Checkpoint Planning Claude Design System.

## Step 1: Upload the files

Download `checkpoint-planning-website.zip` (sent alongside this doc) and
unzip it. It contains everything in `website/`: ten HTML pages,
`styles.css`, `script.js`, `assets/`, and `google-apps-script/Code.gs`.

Upload the **contents** of that folder (not the folder itself,
`index.html` should sit at the root of whatever you upload) to your host
of choice:

- **Netlify / Vercel / Cloudflare Pages:** drag the unzipped folder onto
  their dashboard's "deploy" drop zone, or connect this GitHub repo and
  set the publish/output directory to `website`.
- **GitHub Pages:** push the folder's contents to a `gh-pages` branch (or
  enable Pages on this repo with `website/` as the source directory) in
  Settings → Pages.
- **Shared hosting / cPanel:** upload the files into `checkpointplanning.com`'s
  document root via FTP/SFTP or the file manager.
- **S3 + CloudFront:** upload to an S3 bucket configured for static
  website hosting, with `index.html` as the index document.

## Step 2: Connect the lead form

The two real misconfigurations that were breaking this (deployment
access set to "Only myself" instead of "Anyone", and the Sheet's tab not
being named `Sheet1`) are both fixed as of 2026-09-24, confirmed against
the live deployment with a direct webhook test. `script.js` now also
reads the actual response instead of blindly assuming success, so a
real failure shows the visitor a real error message instead of a false
"thank you."

If lead capture ever breaks again, walk through this in order:

1. **Confirm the deployed Web App is the current code.** In the Google
   Sheet, go to **Extensions → Apps Script**. Paste in the latest
   `website/google-apps-script/Code.gs` (sends Scott an alert email if a
   submission ever fails to save, in addition to the row). Then
   **Deploy → Manage deployments → (pencil/edit icon on the active
   deployment) → Version: New version → Deploy**. Editing the script
   alone does **not** update the live `/exec` URL, you must push a new
   version, this is the single most common reason a working script
   "stops" working after an edit.
2. **Confirm access is set to "Anyone."** Same Manage deployments
   dialog, "Who has access" must be **Anyone** (not "Anyone with Google
   account", not restricted), or every anonymous form submission from a
   site visitor is silently rejected before your code ever runs (no
   Executions log entry, no error email, nothing, this exact symptom is
   what happened here).
3. **Confirm the sheet tab name.** `Code.gs` looks for a tab literally
   named `Sheet1` (the `SHEET_NAME` constant at the top of the file). If
   your tab was renamed, either rename it back to `Sheet1` or edit that
   constant to match, then redeploy (step 1).
4. **Check the Executions log.** In the Apps Script editor, click
   **Executions** in the left sidebar. Submit a test lead, then refresh
   that log. Zero entries at all means the request isn't reaching your
   deployment (steps 1-2), an entry with an error means something inside
   the script failed (the error text says exactly what).
5. **Test the webhook directly**, bypassing the website's hosting and
   caching entirely (swap in your real `/exec` URL):
   ```
   curl -i -X POST "YOUR_EXEC_URL_HERE" \
     -H "Content-Type: text/plain;charset=utf-8" \
     -d '{"name":"Test Lead","email":"test@example.com","transition_type":"Job Loss"}'
   ```
   A working deployment returns `{"result":"success"}`. If you get an
   HTML login/permission page instead, access isn't set to "Anyone"
   (step 2). If you get a script error, the Executions log (step 4) will
   show exactly which line failed.
6. **If the direct test works but the live site still doesn't**, the
   site itself is serving a stale or incorrect `script.js`, not a
   backend problem. Open `https://checkpointplanning.com/script.js`
   directly in a browser (or view-source on any page) and check the
   `LEAD_WEBHOOK_URL` line matches your current deployment exactly. If
   it doesn't, your host cached an old copy, re-upload and hard-refresh
   (or test in a private/incognito window) rather than a normal
   refresh, which can still serve a cached file.
6. Confirm `website/script.js`'s `LEAD_WEBHOOK_URL` constant matches the
   `/exec` URL from your current active deployment (redeploying
   sometimes issues a new URL depending on deployment type), and
   re-upload if it changed.

## Step 3: Guide delivery (no longer relies on email)

The site used to promise "check your inbox" after a lead-magnet
download, but no automation ever actually emailed the guide, that
promise was never fulfilled. It's been replaced: on a successful
submission, the visitor now gets a direct link to their guide on
`resources.html`, an unlisted page (not linked in navigation, marked
`noindex`) rather than a public library page. Nothing to configure here,
just be aware this is how delivery works now, confirm it during your
sanity check below.

## Step 4: Compliance review

Any future content or design changes should go back through your normal
broker-dealer/RIA compliance approval process before you make them live,
the same way the rebrand and the FINRA/SIPC badge-language fix already
did.

## Step 5: Sanity check before sharing a link (ads, email signature, social)

- [ ] All 10 pages load at `checkpointplanning.com` (not just localhost)
- [ ] Submitting a test lead on each page appears as a new row in the
      Google Sheet, not just a success message in the browser
- [ ] The success state after a lead-magnet form shows a working
      download link to the right guide
- [ ] `tel:` and `mailto:` links work on mobile
- [ ] Compliance has signed off on whatever changed since the last review
