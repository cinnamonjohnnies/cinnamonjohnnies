/**
 * Checkpoint Planning, Lead capture webhook
 *
 * Deploy this as a Web App bound to the "Checkpoint Planning - Website Leads"
 * Google Sheet. Full deployment steps are in /docs/SETUP.md.
 *
 * The sheet's header row (already created) is:
 * Timestamp | Name | Email | Phone | Transition Type | Source Page |
 * Message | Lead Magnet Downloaded | UTM Source | UTM Campaign | UTM Medium |
 * UTM Content | Status
 */

const SHEET_NAME = "Sheet1"; // rename if your tab has a different name
const NOTIFY_EMAIL = "scott@checkpointplanning.com"; // set to "" to disable email alerts

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);

  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
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
