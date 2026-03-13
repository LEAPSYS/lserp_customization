import frappe

@frappe.whitelist(allow_guest=True)
def get_theme_css():
    """Dynamically generates CSS variables based on LSERP Theme Settings."""
    if not frappe.db.exists("LSERP Theme Settings", "LSERP Theme Settings"):
        return ""

    theme = frappe.get_doc("LSERP Theme Settings", "LSERP Theme Settings")
    
    if theme.active_theme == "Standard":
        return ""

    css_vars = f"""
    :root {{
        --primary-color: {theme.primary_color or 'var(--primary)'};
        --secondary-color: {theme.secondary_color or 'var(--secondary)'};
        --text-color: {theme.text_color or 'var(--text-color)'};
        --navbar-bg: {theme.background_color or 'var(--navbar-bg)'};
        --sidebar-bg: {theme.sidebar_background or 'var(--sidebar-bg)'};
    }}
    
    /* Global Overrides */
    
    body {{
        background-color: {theme.background_color or 'var(--bg-color)'} !important;
        color: var(--text-color) !important;
    }}
    
    .btn-primary {{
        background-color: var(--primary-color) !important;
        border-color: var(--primary-color) !important;
    }}
    
    .layout-side-section {{
        background-color: var(--sidebar-bg) !important;
    }}
    
    /* More selective overrides for Frappe UI components */
    .standard-sidebar-item.selected, 
    .standard-sidebar-item:hover {{
        background-color: rgba(0,0,0,0.1) !important;
        border-left: 3px solid var(--primary-color);
    }}
    """
    
    frappe.response['type'] = 'download'
    frappe.response['filename'] = 'lserp_theme.css'
    frappe.response['filecontent'] = css_vars.encode('utf-8')
    frappe.response['content_type'] = 'text/css'
    return css_vars
