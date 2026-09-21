/* Checkpoint Planning: shared site behavior
 * Handles lead-capture form submission to the Google Apps Script webhook
 * (see /website/google-apps-script/Code.gs and /docs/SETUP.md for deployment).
 */

// Replace with the /exec URL you get after deploying Code.gs as a Web App.
const LEAD_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwv5y_Vm_gqwIg3aGyEhlnIreE3h180jErOe11J5s7oF0frzq8O57cuADoFZOopFbc/exec";

// Replace with the conversion ID from LinkedIn Campaign Manager > Analyze >
// Conversion Tracking (create a "Lead" conversion action first). The forms
// on this site show an inline success message instead of navigating to a
// new URL, so LinkedIn's URL-based conversion matching won't fire on its
// own; this JS event is what makes LinkedIn conversion tracking work here.
const LINKEDIN_CONVERSION_ID = "REPLACE_WITH_YOUR_LINKEDIN_CONVERSION_ID";

function getUtmParam(name) {
  try {
    return new URLSearchParams(window.location.search).get(name) || "";
  } catch (e) {
    return "";
  }
}

function initLeadForms() {
  const forms = document.querySelectorAll("form[data-lead-form]");
  forms.forEach((form) => {
    // Auto-fill hidden UTM/source fields
    const sourceField = form.querySelector('[name="source_page"]');
    if (sourceField && !sourceField.value) {
      sourceField.value = document.title;
    }
    // Auto-fill any hidden utm_* field (utm_source, utm_medium, utm_campaign,
    // utm_content, utm_term, ...) from the current page's query string.
    form.querySelectorAll('input[type="hidden"][name^="utm_"]').forEach((field) => {
      field.value = getUtmParam(field.name);
    });

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      // Honeypot spam trap, if filled, silently drop the submission.
      const honeypot = form.querySelector('[name="company_website"]');
      if (honeypot && honeypot.value) return;

      const statusEl = form.querySelector(".form-status");
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn ? submitBtn.textContent : "";

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Sending...";
      }
      if (statusEl) {
        statusEl.className = "form-status";
        statusEl.textContent = "";
      }

      const data = Object.fromEntries(new FormData(form).entries());

      if (LEAD_WEBHOOK_URL.startsWith("REPLACE_WITH")) {
        // Fallback while no webhook is configured yet: still show success
        // in the UI during local testing, but warn in the console.
        console.warn(
          "Checkpoint Planning: LEAD_WEBHOOK_URL is not configured. " +
            "See docs/SETUP.md to connect this form to your Google Sheet."
        );
      }

      try {
        if (!LEAD_WEBHOOK_URL.startsWith("REPLACE_WITH")) {
          await fetch(LEAD_WEBHOOK_URL, {
            method: "POST",
            mode: "no-cors", // Apps Script web apps don't return CORS headers
            headers: { "Content-Type": "text/plain;charset=utf-8" },
            body: JSON.stringify(data),
          });
        }

        if (statusEl) {
          statusEl.classList.add("success");
          statusEl.textContent =
            form.dataset.successMessage ||
            "Thank you. Your request has been received. We will be in touch within one business day.";
        }
        form.reset();

        if (window.dataLayer) {
          window.dataLayer.push({
            event: "lead_form_submit",
            form_id: form.id || "lead_form",
            transition_type: data.transition_type || "",
          });
        }

        if (window.lintrk && !LINKEDIN_CONVERSION_ID.startsWith("REPLACE_WITH")) {
          window.lintrk("track", { conversion_id: LINKEDIN_CONVERSION_ID });
        }
      } catch (err) {
        if (statusEl) {
          statusEl.classList.add("error");
          statusEl.textContent =
            "Something went wrong. Please call (949) 702-0139 or email scott@checkpointplanning.com.";
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = originalBtnText;
        }
      }
    });
  });
}

function initMobileMenu() {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");
  if (!toggle || !nav) return;
  toggle.addEventListener("click", () => nav.classList.toggle("open"));
}

document.addEventListener("DOMContentLoaded", () => {
  initLeadForms();
  initMobileMenu();

  // Active year in footer
  const yearEl = document.querySelector("[data-year]");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});
