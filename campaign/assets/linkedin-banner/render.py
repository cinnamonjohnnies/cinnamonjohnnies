# Regenerates website/assets/linkedin-banner.png from banner.html. Edit the
# HTML/CSS in banner.html for any tweaks (copy, colors, motif), then rerun
# this script. Requires: pip install playwright pillow, plus a Chromium
# binary Playwright can find (set CHROME_PATH, or edit the fallback below).
#
# Usage: python3 campaign/assets/linkedin-banner/render.py

import os
from playwright.sync_api import sync_playwright
from PIL import Image

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
HTML_PATH = os.path.join(DIR, "banner.html")
RAW_PATH = os.path.join(DIR, "banner_raw.png")
FINAL_PATH = os.path.join(ROOT, "website", "assets", "linkedin-banner.png")

W, H = 1128, 191
SCALE = 2

with sync_playwright() as p:
    chrome_path = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    browser = p.chromium.launch(executable_path=chrome_path if os.path.exists(chrome_path) else None)
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
    page.goto(f"file://{HTML_PATH}")
    page.wait_for_timeout(150)
    page.screenshot(path=RAW_PATH)
    browser.close()

img = Image.open(RAW_PATH)
print("raw size:", img.size)
img = img.resize((W, H), Image.LANCZOS)
img.save(FINAL_PATH)
print("final size:", img.size, "saved to", FINAL_PATH)
