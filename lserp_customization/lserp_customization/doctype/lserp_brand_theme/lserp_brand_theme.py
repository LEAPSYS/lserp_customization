# Copyright (c) 2024, LEAPSYS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LSERPBrandTheme(Document):
    def before_save(self):
        # Prevent editing predefined themes unless you're a developer
        if self.is_predefined and not frappe.conf.get("developer_mode"):
            frappe.throw(
                "Predefined themes are read-only. Duplicate this theme to customize it.",
                frappe.PermissionError,
            )

    def on_update(self):
        """If this is the currently active theme, flush CSS."""
        settings_exists = frappe.db.exists("LSERP Theme Settings", "LSERP Theme Settings")
        if not settings_exists:
            return
        active = frappe.db.get_single_value("LSERP Theme Settings", "active_theme")
        if active == self.name:
            frappe.clear_cache()
