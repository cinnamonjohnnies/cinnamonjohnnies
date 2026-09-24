/**
 * Checkpoint Planning, Lead capture webhook
 *
 * Deploy this as a Web App bound to the "Checkpoint Planning - Website Leads"
 * Google Sheet. Full deployment steps are in /docs/SETUP.md and /docs/DEPLOY.md.
 *
 * IMPORTANT: the website form posts with mode:"no-cors", so the browser can
 * never tell the visitor (or you, from the JS console) whether this actually
 * succeeded, it always shows a success message regardless. The Google Sheet
 * and the failure-alert email below are the only real signal. If you edit
 * this file, you MUST push a new version (Deploy -> Manage deployments ->
 * edit the active deployment -> Version: New version -> Deploy), editing the
 * script alone does not update the live /exec URL.
 *
 * The sheet's header row (already created) is:
 * Timestamp | Name | Email | Phone | Transition Type | Source Page |
 * Message | Lead Magnet Downloaded | UTM Source | UTM Campaign | UTM Medium |
 * UTM Content | Status
 */

const SHEET_NAME = "Sheet1"; // must match your tab's actual name exactly
const NOTIFY_EMAIL = "scott@checkpointplanning.com"; // set to "" to disable email alerts

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);

  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    if (!sheet) {
      throw new Error(
        'No tab named "' + SHEET_NAME + '" found in this spreadsheet. ' +
        "Check the SHEET_NAME constant against your actual tab name."
      );
    }

    const data = JSON.parse(e.postData.contents);

    const row = [
      new Date(),
      data.name || "",
      data.email || "",
      data.phone || "",
      data.transition_type || "",
      data.source_page || "",
      data.message || "",
      data.lead_magnet || "",
      data.utm_source || "",
      data.utm_campaign || "",
      data.utm_medium || "",
      data.utm_content || "",
      "New",
    ];

    sheet.appendRow(row);

    if (NOTIFY_EMAIL) {
      MailApp.sendEmail({
        to: NOTIFY_EMAIL,
        subject: "New Checkpoint Planning website lead: " + (data.name || "Unknown"),
        body:
          "A new lead came in from the website.\n\n" +
          "Name: " + (data.name || "") + "\n" +
          "Email: " + (data.email || "") + "\n" +
          "Phone: " + (data.phone || "") + "\n" +
          "Transition: " + (data.transition_type || "") + "\n" +
          "Source page: " + (data.source_page || "") + "\n" +
          "Lead magnet: " + (data.lead_magnet || "") + "\n" +
          "Message:\n" + (data.message || "") + "\n\n" +
          "View the full lead list in the Checkpoint Planning - Website Leads sheet.",
      });
    }

    return ContentService.createTextOutput(
      JSON.stringify({ result: "success" })
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    // The website can never see this (no-cors), so this alert email is the
    // only way a failed submission won't just silently vanish.
    if (NOTIFY_EMAIL) {
      try {
        MailApp.sendEmail({
          to: NOTIFY_EMAIL,
          subject: "Checkpoint Planning website lead FAILED to save",
          body:
            "A website visitor submitted a form, saw a success message, but " +
            "the lead was NOT saved to the Sheet. Error:\n\n" + String(err) +
            "\n\nRaw submission:\n" + (e && e.postData && e.postData.contents ? e.postData.contents : "(none)"),
        });
      } catch (mailErr) {
        // Nothing more we can do if even the alert email fails.
      }
    }
    return ContentService.createTextOutput(
      JSON.stringify({ result: "error", error: String(err) })
    ).setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return ContentService.createTextOutput(
    "Checkpoint Planning lead intake endpoint is running."
  );
}
