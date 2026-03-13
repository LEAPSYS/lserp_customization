import frappe

def extend_bootinfo(bootinfo):
    """Injects LSERP Theme Details into frappe.boot on every page load."""
    if not frappe.db.exists("LSERP Theme Settings", "LSERP Theme Settings"):
        return

    theme = frappe.get_doc("LSERP Theme Settings", "LSERP Theme Settings")
    bootinfo.lserp_theme = {
        "brand_name": theme.brand_name or "",
        "brand_logo": theme.brand_logo or "",
        "active_theme": theme.active_theme or "Standard"
    }
