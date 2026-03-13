# Copyright (c) 2024, LEAPSYS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
from bs4 import BeautifulSoup
import re


# ─────────────────────────────────────────────────────────────────────────────
#  Predefined Brand Theme Presets
# ─────────────────────────────────────────────────────────────────────────────
THEMES = {
    "LS Theme": {
        # Colors extracted from leapsys.net
        "primary_color":    "#E1251B",  # LEAPSYS signature red
        "secondary_color":  "#1D1D1B",  # Near-black
        "text_color":       "#333333",
        "background_color": "#FFFFFF",
        "sidebar_background": "#E1251B",
        "font_family":      "Inter",
        "brand_name":       "LEAPSYS",
    },
    "Enummo Theme": {
        # Colors extracted live from enumoo.com  (March 2024)
        # Primary: Teal  #078586  (navbar accent, CTA button, logo accent)
        # Dark BG: #282f3b  (header / dark sections)
        # Light BG: #f0f3f9
        "primary_color":    "#078586",  # Enumoo teal
        "secondary_color":  "#282f3b",  # Dark navy/slate
        "text_color":       "#4a4e56",  # Enumoo body text dark gray
        "background_color": "#f0f3f9",  # Enumoo light bg
        "sidebar_background": "#1f2530",  # Enumoo footer dark
        "font_family":      "Inter",    # Enumoo body font
        "brand_name":       "Enumoo",
    },
}


class LSERPThemeSettings(Document):

    @frappe.whitelist()
    def extract_colors_from_url(self):
        """Scrape the provided URL and extract dominant brand colors."""
        if not self.website_url:
            frappe.throw("Please provide a Website URL.")

        try:
            url = self.website_url if self.website_url.startswith("http") else f"https://{self.website_url}"
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # 1. Meta theme-color
            theme_color_tag = soup.find("meta", attrs={"name": "theme-color"})
            if theme_color_tag and theme_color_tag.get("content"):
                primary_hex = theme_color_tag["content"]
                self.primary_color = primary_hex
                self.sidebar_background = primary_hex
                frappe.msgprint(f"Extracted Primary Color {primary_hex} from meta tag.")
                return

            # 2. CSS variables  (--primary-color: #xxx)
            styles = " ".join(s.text for s in soup.find_all("style"))
            css_vars = re.findall(r"--[\w-]+\s*:\s*(#(?:[0-9a-fA-F]{3}){1,2})", styles)
            hex_colors = re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", styles)

            candidate = (css_vars + hex_colors)
            if candidate:
                # Filter out near-white / near-black generic colours
                from collections import Counter
                filtered = [c for c in candidate if c.lower() not in ("#fff", "#ffffff", "#000", "#000000")]
                if filtered:
                    most_common = Counter(filtered).most_common(1)[0][0]
                    self.primary_color = most_common
                    frappe.msgprint(f"Extracted dominant color {most_common} from CSS.")
                    return

            frappe.msgprint("Could not auto-detect colors. Please set them manually.")

        except Exception as exc:
            frappe.throw(f"Error fetching URL: {exc}")

    # ------------------------------------------------------------------
    def validate(self):
        self._apply_preset_theme()
        self.apply_whitelabel_settings()

    # ------------------------------------------------------------------
    def _apply_preset_theme(self):
        """If a predefined theme is selected, overwrite the color fields."""
        preset = THEMES.get(self.active_theme)
        if not preset:
            return

        for field, value in preset.items():
            if hasattr(self, field):
                # Only overwrite if the user hasn't already customised the field,
                # or if the theme itself just changed (simplest: always apply preset).
                setattr(self, field, value)

    # ------------------------------------------------------------------
    def apply_whitelabel_settings(self):
        """Push brand name + logo into Frappe core settings."""
        try:
            if self.brand_name:
                sys = frappe.get_doc("System Settings", "System Settings")
                if sys.app_name != self.brand_name:
                    sys.app_name = self.brand_name
                    sys.save(ignore_permissions=True)

            if self.brand_logo:
                navbar = frappe.get_doc("Navbar Settings", "Navbar Settings")
                if navbar.app_logo != self.brand_logo:
                    navbar.app_logo = self.brand_logo
                    navbar.save(ignore_permissions=True)

                web = frappe.get_doc("Website Settings", "Website Settings")
                if web.app_logo != self.brand_logo or web.splash_image != self.brand_logo:
                    web.app_logo = self.brand_logo
                    web.splash_image = self.brand_logo
                    web.save(ignore_permissions=True)

                # site_config for very early loads (login page logo)
                from frappe.installer import update_site_config
                update_site_config("app_logo_url", self.brand_logo)

            frappe.clear_cache()

        except Exception as exc:
            frappe.log_error(f"Whitelabel error: {exc}", "LSERP Theme Whitelabel")
