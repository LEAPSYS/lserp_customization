import frappe


# ──────────────────────────────────────────────────────────────────────────────
#  Main desk theme (all internal pages)
# ──────────────────────────────────────────────────────────────────────────────
@frappe.whitelist(allow_guest=True)
def get_theme_css():
    """Dynamically generates CSS for ALL internal Frappe pages based on LSERP Theme Settings."""
    if not frappe.db.exists("LSERP Theme Settings", "LSERP Theme Settings"):
        return ""

    theme = frappe.get_doc("LSERP Theme Settings", "LSERP Theme Settings")

    if theme.active_theme == "Standard" and not theme.enable_modern_dashboard:
        return ""

    primary   = theme.primary_color   or "#078586"
    secondary = theme.secondary_color or "#282f3b"
    bg        = theme.background_color or "#f0f3f9"
    text      = theme.text_color      or "#1a1a2e"
    sidebar   = theme.sidebar_background or "#1f2530"
    modern    = bool(theme.enable_modern_dashboard)

    font = getattr(theme, "font_family", "Inter") or "Inter"
    font_url_map = {
        "Inter":   "Inter:wght@300;400;500;600;700",
        "Outfit":  "Outfit:wght@300;400;500;600;700",
        "Roboto":  "Roboto:wght@300;400;500;700",
        "DM Sans": "DM+Sans:wght@300;400;500;600;700",
    }
    font_url = font_url_map.get(font, font_url_map["Inter"])

    # Primary lighter shade for hover / highlights (simple darken trick via opacity)
    primary_alpha = primary + "22"   # 13 % opacity overlay

    css = f"""
/* ================================================================
   LSERP Theme  — generated for all internal Frappe/ERPNext pages
   Theme: {theme.active_theme}  |  Modern: {modern}
   ================================================================ */

/* ---------- 0. Custom font ---------- */
@import url('https://fonts.googleapis.com/css2?family={font_url}&display=swap');

html, body, .frappe-app,
input, textarea, select, button,
.form-control, .frappe-control {{ font-family: '{font}', sans-serif !important; }}

/* ---------- 1. CSS variables ---------- */
:root {{
    --lserp-primary:    {primary};
    --lserp-secondary:  {secondary};
    --lserp-bg:         {bg};
    --lserp-text:       {text};
    --lserp-sidebar:    {sidebar};
}}

/* ================================================================
   NAVBAR / TOP BAR
   ================================================================ */
.navbar,
.page-header,
.desk-navbar {{
    background: linear-gradient(135deg, {secondary} 0%, {primary} 100%) !important;
    border-bottom: none !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.18) !important;
}}
.navbar .navbar-brand,
.navbar a,
.navbar .btn,
.navbar .search-bar input,
.navbar .form-control,
.navbar .notifications-icon,
.navbar .input-group-text,
.navbar .nav-link {{
    color: #fff !important;
}}
.navbar .search-bar input::placeholder {{
    color: rgba(255,255,255,0.65) !important;
}}
.navbar .search-bar,
.navbar .input-group {{
    background: rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
}}

/* ================================================================
   LEFT SIDEBAR / DESK MENU
   ================================================================ */
.layout-side-section,
.desk-sidebar,
.sidebar-column,
.sidebar,
.sidebar-menu {{
    background: {sidebar} !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}}
.sidebar-item,
.sidebar-item a,
.desk-sidebar .sidebar-group-title,
.sidebar-label {{
    color: rgba(255,255,255,0.75) !important;
}}
.sidebar-item:hover,
.standard-sidebar-item:hover {{
    background: rgba(255,255,255,0.08) !important;
    color: #fff !important;
    border-left: 3px solid {primary} !important;
}}
.standard-sidebar-item.selected,
.sidebar-item.active {{
    background: rgba(255,255,255,0.14) !important;
    color: #fff !important;
    border-left: 3px solid {primary} !important;
    font-weight: 600 !important;
}}

/* ================================================================
   PAGE CONTENT BACKGROUND
   ================================================================ */
.page-container,
.main-section,
.layout-main,
.desk-body,
.page-content {{
    background: {bg} !important;
}}

/* ================================================================
   FORM VIEWS  (DocType form pages)
   ================================================================ */
.form-page,
.page-form,
.frappe-doc-section,
.form-section {{
    background: #fff !important;
    border-radius: {'12px' if modern else '4px'} !important;
    border: 1px solid rgba(0,0,0,0.07) !important;
    box-shadow: {'rgba(100,100,111,0.10) 0px 6px 20px 0px' if modern else 'none'} !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
}}

/* Section heading */
.section-head,
.form-section-heading,
.section-title {{
    color: {secondary} !important;
    font-weight: 600 !important;
    border-bottom: 2px solid {primary}33 !important;
    padding-bottom: 6px !important;
}}

/* Field labels */
.control-label,
.frappe-control label,
.label-area {{
    color: {text} !important;
    font-weight: 500 !important;
}}

/* Input fields */
.form-control,
.frappe-control .form-control,
.input-with-feedback,
.ql-container {{
    border-radius: {'8px' if modern else '4px'} !important;
    border: 1.5px solid #dde2e8 !important;
    background: #fafbfc !important;
    color: {text} !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}
.form-control:focus,
.frappe-control .form-control:focus {{
    border-color: {primary} !important;
    box-shadow: 0 0 0 3px {primary_alpha} !important;
    background: #fff !important;
    outline: none !important;
}}

/* ================================================================
   BUTTONS
   ================================================================ */
.btn-primary,
.btn.btn-primary {{
    background: linear-gradient(135deg, {primary} 0%, {secondary} 100%) !important;
    border: none !important;
    border-radius: {'10px' if modern else '4px'} !important;
    font-weight: 600 !important;
    color: #fff !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.15) !important;
    transition: transform 0.15s ease, box-shadow 0.2s ease !important;
}}
.btn-primary:hover, .btn.btn-primary:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.2) !important;
    opacity: 0.95 !important;
}}

.btn-secondary, .btn-default {{
    background: #fff !important;
    border: 1.5px solid {primary} !important;
    color: {primary} !important;
    border-radius: {'10px' if modern else '4px'} !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
}}
.btn-secondary:hover, .btn-default:hover {{
    background: {primary} !important;
    color: #fff !important;
}}

.btn-danger {{ border-radius: {'10px' if modern else '4px'} !important; }}

/* ================================================================
   LIST VIEWS (e.g., Student List, Invoice List)
   ================================================================ */
.list-container,
.result,
.list-row,
.list-item {{
    background: #fff !important;
    border-radius: {'10px' if modern else '2px'} !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
    box-shadow: {'rgba(100,100,111,0.08) 0px 4px 14px' if modern else 'none'} !important;
    transition: transform 0.15s ease, box-shadow 0.2s ease !important;
}}
.list-row:hover {{
    background: {primary_alpha} !important;
    transform: {'translateX(2px)' if modern else 'none'} !important;
}}

/* List header */
.list-row-head,
.list-header {{
    background: {secondary}0D !important;
    color: {secondary} !important;
    font-weight: 600 !important;
    border-radius: {'10px 10px 0 0' if modern else '0'} !important;
}}

/* List checkboxes / stars */
.list-subject a,
.list-row a {{
    color: {primary} !important;
}}

/* ================================================================
   DATA TABLES (Report & List Grid)
   ================================================================ */
.dt-header-row th,
.datatable .dt-cell--header {{
    background: {secondary} !important;
    color: #fff !important;
    font-weight: 600 !important;
}}
.datatable .dt-row:hover .dt-cell {{
    background: {primary_alpha} !important;
}}
.datatable .dt-cell {{ border-color: rgba(0,0,0,0.05) !important; }}

/* ================================================================
   DIALOG / MODAL
   ================================================================ */
.modal-content {{
    border-radius: {'16px' if modern else '6px'} !important;
    border: none !important;
    box-shadow: 0 24px 64px rgba(0,0,0,0.22) !important;
}}
.modal-header {{
    background: linear-gradient(135deg, {secondary}, {primary}) !important;
    color: #fff !important;
    border-radius: {'16px 16px 0 0' if modern else '6px 6px 0 0'} !important;
    border-bottom: none !important;
    padding: 18px 24px !important;
}}
.modal-header .modal-title,
.modal-header h4,
.modal-header h5 {{ color: #fff !important; font-weight: 700 !important; }}
.modal-header .close {{ color: rgba(255,255,255,0.8) !important; }}
.modal-body {{ padding: 24px !important; }}
.modal-footer {{
    border-top: 1px solid rgba(0,0,0,0.07) !important;
    padding: 16px 24px !important;
}}

/* ================================================================
   TABS
   ================================================================ */
.nav-tabs .nav-link.active,
.form-tabs-list .nav-link.active {{
    color: {primary} !important;
    border-bottom: 3px solid {primary} !important;
    font-weight: 600 !important;
    background: transparent !important;
}}
.nav-tabs .nav-link:hover {{
    color: {primary} !important;
    border-bottom: 2px solid {primary}55 !important;
}}

/* ================================================================
   BREADCRUMBS & PAGE TITLE
   ================================================================ */
.breadcrumb-area .breadcrumb-item a {{
    color: {primary} !important;
}}
.page-title,
.title-text {{
    color: {secondary} !important;
    font-weight: 700 !important;
}}

/* ================================================================
   BADGES / INDICATORS
   ================================================================ */
.indicator-pill.green  {{ background: #e6f8f1 !important; color: #1a9c6b !important; }}
.indicator-pill.yellow {{ background: #fef9e7 !important; color: #c9a700 !important; }}
.indicator-pill.red    {{ background: #fdecea !important; color: #c0392b !important; }}
.indicator-pill.blue   {{ background: {primary_alpha} !important; color: {primary} !important; }}

/* ================================================================
   ALERTS / TOASTS
   ================================================================ */
.alert-primary {{ border-left: 4px solid {primary} !important; }}

/* ================================================================
   WORKSPACE (Dashboard home)
   ================================================================ */
.widget,
.shortcut-widget-box,
.dashboard-widget-box,
.frappe-card {{
    background: rgba(255,255,255,{'0.80' if modern else '1.0'}) !important;
    border-radius: {'14px' if modern else '6px'} !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
    box-shadow: {'rgba(100,100,111,0.12) 0px 8px 24px' if modern else '0 1px 4px rgba(0,0,0,0.08)'} !important;
    transition: box-shadow 0.25s ease, transform 0.2s ease !important;
}}
.widget:hover, .shortcut-widget-box:hover {{
    transform: {'translateY(-3px)' if modern else 'none'} !important;
    box-shadow: {'rgba(100,100,111,0.22) 0px 14px 30px' if modern else '0 4px 12px rgba(0,0,0,0.10)'} !important;
}}

/* ================================================================
   REPORTS
   ================================================================ */
.report-wrapper,
.report-summary-wrapper {{ background: {bg} !important; }}

.chart-container {{
    background: #fff !important;
    border-radius: {'12px' if modern else '4px'} !important;
    box-shadow: {'rgba(100,100,111,0.10) 0px 6px 20px' if modern else 'none'} !important;
    padding: 16px !important;
}}

/* ================================================================
   SCROLLBAR (global)
   ================================================================ */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: {primary}66;
    border-radius: 6px;
}}
::-webkit-scrollbar-thumb:hover {{ background: {primary}; }}

/* ================================================================
   PRINT overrides – keep clean
   ================================================================ */
@media print {{
    .navbar, .layout-side-section {{ display: none !important; }}
    body {{ background: #fff !important; font-family: '{font}', sans-serif !important; }}
}}
"""
    return css


# ──────────────────────────────────────────────────────────────────────────────
#  Login page  (served as guest)
# ──────────────────────────────────────────────────────────────────────────────
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

.login-content, .page-card, .form-login-wrapper {{
    background: rgba(255, 255, 255, 0.97) !important;
    border-radius: 20px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25) !important;
    padding: 40px !important;
    border: none !important;
}}

.login-content h2, .page-card h2, .page-card h3 {{
    color: {secondary} !important;
    font-weight: 700 !important;
}}

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

.login-content .form-control, .page-card .form-control {{
    border-radius: 8px !important;
    border: 1.5px solid #e0e0e0 !important;
}}
.login-content .form-control:focus, .page-card .form-control:focus {{
    border-color: {primary} !important;
    box-shadow: 0 0 0 3px {primary}33 !important;
}}

.login-content a, .page-card a {{ color: {primary} !important; }}
"""
