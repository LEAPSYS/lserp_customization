# Copyright (c) 2024, LEAPSYS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LSERPThemeSettings(Document):
    def validate(self):
        """When saving, apply whitelabel settings from the linked theme."""
        if not self.active_theme:
            return
        if not frappe.db.exists("LSERP Brand Theme", self.active_theme):
            frappe.throw(f"Theme '{self.active_theme}' not found.")
        self.apply_whitelabel_settings()

    def apply_whitelabel_settings(self):
        """Sync brand_name + brand_logo from the linked theme into Frappe core settings."""
        try:
            theme = frappe.get_doc("LSERP Brand Theme", self.active_theme)

            if theme.brand_name:
                sys = frappe.get_doc("System Settings", "System Settings")
                if sys.app_name != theme.brand_name:
                    sys.app_name = theme.brand_name
                    sys.save(ignore_permissions=True)

            if theme.brand_logo:
                try:
                    navbar = frappe.get_doc("Navbar Settings", "Navbar Settings")
                    if navbar.app_logo != theme.brand_logo:
                        navbar.app_logo = theme.brand_logo
                        navbar.save(ignore_permissions=True)
                except Exception:
                    pass

                try:
                    web = frappe.get_doc("Website Settings", "Website Settings")
                    if web.app_logo != theme.brand_logo or web.splash_image != theme.brand_logo:
                        web.app_logo = theme.brand_logo
                        web.splash_image = theme.brand_logo
                        web.save(ignore_permissions=True)
                except Exception:
                    pass

                try:
                    from frappe.installer import update_site_config
                    update_site_config("app_logo_url", theme.brand_logo)
                except Exception:
                    pass

            frappe.clear_cache()

        except Exception as exc:
            frappe.log_error(f"Whitelabel update error: {exc}", "LSERP Theme Whitelabel")
