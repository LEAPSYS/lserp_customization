import frappe
from lserp_customization import __version__


def extend_bootinfo(bootinfo):
    """Injects active LSERP Brand Theme data into frappe.boot for frontend use."""
    try:
        if not frappe.db.exists("LSERP Theme Settings", "LSERP Theme Settings"):
            return

        active_name = frappe.db.get_single_value("LSERP Theme Settings", "active_theme")
        if not active_name:
            return

        if not frappe.db.exists("LSERP Brand Theme", active_name):
            return

        theme = frappe.get_doc("LSERP Brand Theme", active_name)
        bootinfo.lserp_theme = {
            "theme_name":              theme.theme_name,
            "brand_name":              theme.brand_name or "",
            "brand_logo":              theme.brand_logo or "",
            "primary_color":           theme.primary_color or "",
            "secondary_color":         theme.secondary_color or "",
            "background_color":        theme.background_color or "",
            "font_family":             theme.font_family or "Inter",
            "enable_modern_dashboard": bool(theme.enable_modern_dashboard),
            "app_version":             __version__,
        }
    except Exception as exc:
        frappe.log_error(f"boot.py error: {exc}", "LSERP Boot")
