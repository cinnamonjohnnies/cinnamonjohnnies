# Deploying to start.checkpointplanning.com

This covers going live on a new subdomain (`start.checkpointplanning.com`)
while `checkpointplanning.com` stays untouched for now. The site is fully
static, any host that serves plain files works. Pick whichever matches how
you already manage checkpointplanning.com's DNS/hosting.

The site now includes the full "base" site, Home, About, Services, Our
Process, Fees, and Contact, built to match your real branding (logo, icon
mark, CRPC badge), plus the four transition landing pages (Job Loss,
Early Retirement, Divorce, Inheritance). Once this clears compliance
review, you can either keep it running at the subdomain permanently, or
swap the DNS so it becomes the new checkpointplanning.com, same files,
just a later decision.

## Step 1: Upload the files

Download `checkpoint-planning-website.zip` (sent alongside this doc) and
unzip it. It contains everything in `website/`: ten HTML pages, `styles.css`,
`script.js`, `assets/` (your logo, icon mark, CRPC badge, and headshot), and
`google-apps-script/Code.gs`.

Upload the **contents** of that folder (not the folder itself, `index.html`
should sit at the root of whatever you upload) to your host of choice:

- **Netlify / Vercel / Cloudflare Pages:** drag the unzipped folder onto
  their dashboard's "deploy" drop zone, or connect this GitHub repo and set
  the publish/output directory to `website`.
- **GitHub Pages:** push the folder's contents to a `gh-pages` branch (or
  enable Pages on this repo with `website/` as the source directory) in
  Settings → Pages.
- **Shared hosting / cPanel (if checkpointplanning.com uses this):** create
  a subdomain `start` in your hosting control panel, then upload the files
  into that subdomain's document root via FTP/SFTP or the file manager.
- **S3 + CloudFront:** upload to an S3 bucket configured for static website
  hosting, with `index.html` as the index document.

## Step 2: Point the subdomain at it

In whatever service manages DNS for checkpointplanning.com (likely your
domain registrar or a host like GoDaddy, Namecheap, Cloudflare, or your
hosting provider):

- **If using Netlify/Vercel/Cloudflare Pages:** add a `CNAME` record for
  `start` pointing to the hostname they give you after deploy (e.g.
  `your-site-name.netlify.app`), then add `start.checkpointplanning.com`
  as a custom domain in that platform's dashboard.
- **If using GitHub Pages:** add a `CNAME` record for `start` pointing to
  `<your-github-username>.github.io`, and add a `CNAME` file containing
  `start.checkpointplanning.com` to the published folder.
- **If using shared hosting under the same account as checkpointplanning.com:**
  the subdomain and DNS are usually handled together in your host's control
  panel, creating the subdomain in Step 1 may already set up DNS for you.

DNS changes can take a few minutes to a few hours to propagate.

## Step 3: Connect the lead form (do this before sharing the link)

The forms won't save leads anywhere until you deploy the Google Apps
Script webhook, see `docs/SETUP.md` for the 5-minute walkthrough. Until
that's done, submissions will show a success message in the browser but
nothing will be recorded. Test by submitting the form yourself and
checking the "Checkpoint Planning - Website Leads" Google Sheet.

## Step 4: Compliance review

As noted in `docs/SETUP.md`, run the live pages, the three new lead
magnets, and the email sequences through your normal broker-dealer/RIA
compliance approval process before promoting the link anywhere (ads,
email signature, social).

## Step 5: Sanity check before sharing

- [ ] All 5 pages load at the new subdomain (not just localhost)
- [ ] Submitting a test lead on each page appears in the Google Sheet
- [ ] `tel:` and `mailto:` links work on mobile
- [ ] Compliance has signed off
