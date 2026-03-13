import frappe

@frappe.whitelist(allow_guest=True)
def get_theme_css():
    """Dynamically generates CSS variables + modern dashboard overrides based on LSERP Theme Settings."""
    if not frappe.db.exists("LSERP Theme Settings", "LSERP Theme Settings"):
        return ""

    theme = frappe.get_doc("LSERP Theme Settings", "LSERP Theme Settings")

    if theme.active_theme == "Standard" and not theme.enable_modern_dashboard:
        return ""

    primary   = theme.primary_color  or "#5f67ea"
    secondary = theme.secondary_color or "#34c79a"
    bg        = theme.background_color or "#f4f5f7"
    text      = theme.text_color or "#1a1a2e"
    sidebar   = theme.sidebar_background or "#ffffff"

    # ------------------------------------------------------------------ #
    #  1. Base color variables + basic overrides                          #
    # ------------------------------------------------------------------ #
    css = f"""
/* ======================================================
   LSERP Dynamic Theme  –  auto-generated
   ====================================================== */
:root {{
    --lserp-primary:   {primary};
    --lserp-secondary: {secondary};
    --lserp-text:      {text};
    --lserp-bg:        {bg};
    --lserp-sidebar:   {sidebar};
}}

/* Navbar */
.navbar {{
    background-color: {primary} !important;
}}
.navbar .navbar-brand, .navbar a, .navbar .notifications-icon,
.navbar .search-bar input, .navbar .form-control {{
    color: #fff !important;
}}

/* Sidebar */
.layout-side-section, .desk-sidebar, .sidebar-column {{
    background-color: {sidebar} !important;
}}

/* Button Primary */
.btn-primary {{
    background-color: {primary} !important;
    border-color:     {primary} !important;
}}
.btn-primary:hover {{
    background-color: {secondary} !important;
    border-color:     {secondary} !important;
}}

/* Sidebar active */
.standard-sidebar-item.selected,
.standard-sidebar-item:hover {{
    background-color: rgba(0,0,0,0.07) !important;
    border-left: 3px solid {primary};
}}

/* Page background */
.page-container, .main-section, .layout-main {{
    background-color: {bg} !important;
}}
"""

    # ------------------------------------------------------------------ #
    #  2. Modern / Glassmorphism dashboard layer                          #
    # ------------------------------------------------------------------ #
    if theme.enable_modern_dashboard:
        font = getattr(theme, "font_family", "Inter") or "Inter"
        font_url_map = {
            "Inter":   "Inter:wght@300;400;500;600;700",
            "Outfit":  "Outfit:wght@300;400;500;600;700",
            "Roboto":  "Roboto:wght@300;400;500;700",
            "DM Sans": "DM+Sans:wght@300;400;500;600;700",
        }
        font_url = font_url_map.get(font, font_url_map["Inter"])

        css += f"""
/* ======================================================
   LSERP Modern Dashboard Overrides
   ====================================================== */

/* ---------- 1. Typography ---------- */
@import url('https://fonts.googleapis.com/css2?family={font_url}&display=swap');

html, body, .desk-container, .frappe-app,
input, button, select, textarea, .form-control {{
    font-family: '{font}', sans-serif !important;
}}

/* ---------- 2. Card / Widget glassmorphism ---------- */
.widget, .widget-group, .shortcut-widget-box,
.dashboard-widget-box, .onboarding-widget-box,
.workspace-section-header, .widget.shortcut-widget-box,
.report-summary-wrapper, .chart-container,
.frappe-card, .list-item, .notification-item {{
    background: rgba(255,255,255,0.75) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
    box-shadow: rgba(100,100,111,0.12) 0px 8px 24px 0px !important;
    transition: box-shadow 0.25s ease, transform 0.2s ease !important;
}}

/* Hover lift */
.widget:hover, .shortcut-widget-box:hover, .frappe-card:hover {{
    transform: translateY(-3px) !important;
    box-shadow: rgba(100,100,111,0.22) 0px 14px 30px 0px !important;
}}

/* ---------- 3. Workspace Header ---------- */
.workspace-container h1,
.workspace-container .workspace-title,
.page-head .title-area h3 {{
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
    color: {text} !important;
}}

/* ---------- 4. Shortcut Badges  ---------- */
.shortcut-widget-box .widget-head .widget-title {{
    font-weight: 600 !important;
    color: {primary} !important;
}}

/* ---------- 5. Sidebar refinements ---------- */
.sidebar-column,
.layout-side-section {{
    background: rgba(255,255,255,0.8) !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
    border-right: 1px solid rgba(0,0,0,0.06) !important;
}}

/* ---------- 6. Navbar ---------- */
.navbar {{
    background: linear-gradient(135deg, {primary}, {secondary}) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    border-bottom: none !important;
}}

/* ---------- 7. Page Content Area ---------- */
.page-container {{
    background: {bg} !important;
    min-height: 100vh !important;
}}

/* ---------- 8. Scrollbar ---------- */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: rgba(0,0,0,0.15);
    border-radius: 6px;
}}
::-webkit-scrollbar-thumb:hover {{ background: rgba(0,0,0,0.25); }}

/* ---------- 9. Smooth animations ---------- */
.frappe-app * {{
    transition: background-color 0.15s ease, box-shadow 0.2s ease !important;
}}
"""

    return css


@frappe.whitelist(allow_guest=True)
def get_login_page_css():
    """Returns branded CSS specifically for the Frappe login page."""
    if not frappe.db.exists("LSERP Theme Settings", "LSERP Theme Settings"):
        return ""

    theme = frappe.get_doc("LSERP Theme Settings", "LSERP Theme Settings")

    primary   = theme.primary_color   or "#078586"
    secondary = theme.secondary_color or "#282f3b"
    font      = getattr(theme, "font_family", "Inter") or "Inter"
    font_url_map = {
        "Inter":   "Inter:wght@300;400;500;600;700",
        "Outfit":  "Outfit:wght@300;400;500;600;700",
        "Roboto":  "Roboto:wght@300;400;500;700",
        "DM Sans": "DM+Sans:wght@300;400;500;600;700",
    }
    font_url = font_url_map.get(font, font_url_map["Inter"])

    return f"""
@import url('https://fonts.googleapis.com/css2?family={font_url}&display=swap');

body {{
    font-family: '{font}', sans-serif !important;
    background: linear-gradient(135deg, {secondary} 0%, {primary} 100%) !important;
    min-height: 100vh;
}}

/* Login card */
.login-content, .page-card, .form-login-wrapper {{
    background: rgba(255, 255, 255, 0.97) !important;
    border-radius: 20px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25) !important;
    padding: 40px !important;
    border: none !important;
}}

/* Heading */
.login-content h2, .page-card h2, .page-card h3 {{
    color: {secondary} !important;
    font-weight: 700 !important;
}}

/* Submit button */
.login-content .btn-primary, .page-card .btn-primary {{
    background: linear-gradient(135deg, {primary}, {secondary}) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    width: 100% !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    transition: opacity 0.2s, transform 0.15s !important;
}}
.login-content .btn-primary:hover, .page-card .btn-primary:hover {{
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}}

/* Inputs */
.login-content .form-control, .page-card .form-control {{
    border-radius: 8px !important;
    border: 1.5px solid #e0e0e0 !important;
}}
.login-content .form-control:focus, .page-card .form-control:focus {{
    border-color: {primary} !important;
    box-shadow: 0 0 0 3px {primary}33 !important;
}}

/* Links */
.login-content a, .page-card a {{ color: {primary} !important; }}
"""
