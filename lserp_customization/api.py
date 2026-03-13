import frappe


# ──────────────────────────────────────────────────────────────────────────────
#  Main desk theme (all internal pages)
# ──────────────────────────────────────────────────────────────────────────────
@frappe.whitelist(allow_guest=True)
def get_theme_css():
    """Override Frappe's native CSS variable system + all internal pages."""
    if not frappe.db.exists("LSERP Theme Settings", "LSERP Theme Settings"):
        return ""

    theme = frappe.get_doc("LSERP Theme Settings", "LSERP Theme Settings")

    if theme.active_theme == "Standard" and not getattr(theme, "enable_modern_dashboard", 0):
        return ""

    p  = theme.primary_color   or "#078586"   # Primary brand teal
    s  = theme.secondary_color or "#282f3b"   # Dark navy
    bg = theme.background_color or "#f0f3f9"  # Page bg
    tx = theme.text_color       or "#282f3b"
    sb = theme.sidebar_background or "#1f2530"

    modern = bool(getattr(theme, "enable_modern_dashboard", 0))
    font   = getattr(theme, "font_family", "Inter") or "Inter"

    font_url_map = {
        "Inter":   "Inter:wght@300;400;500;600;700",
        "Outfit":  "Outfit:wght@300;400;500;600;700",
        "Roboto":  "Roboto:wght@300;400;500;700",
        "DM Sans": "DM+Sans:wght@300;400;500;600;700",
    }
    font_url = font_url_map.get(font, font_url_map["Inter"])

    r = "12px" if modern else "6px"      # border-radius token
    r_sm = "8px" if modern else "4px"
    r_lg = "16px" if modern else "8px"

    css = f"""
/* ================================================================
   LSERP Theme Override  –  All Internal Pages
   ================================================================ */

/* ── 0. Font ─────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family={font_url}&display=swap');

html, body, input, button, select, textarea,
.form-control, .frappe-control, .btn, .sidebar-item {{
    font-family: '{font}', sans-serif !important;
}}

/* ================================================================
   1. FRAPPE CSS VARIABLE OVERRIDES  (the critical step)
      These shadow Frappe's own design tokens so every
      component that reads them gets our brand colours.
   ================================================================ */
:root,
[data-theme="light"],
[data-theme="dark"] {{

    /* primary */
    --primary:            {p};
    --primary-color:      {p};
    --brand-color:        {p};
    --btn-primary:        {p};
    --progress-bar-bg:    {p};

    /* navbar */
    --navbar-bg:          {s};

    /* sidebar */
    --sidebar-select-color: rgba(255,255,255,0.12);

    /* background layers */
    --bg-color:           {bg};
    --subtle-accent:      {bg};
    --subtle-fg:          {bg};

    /* card / fg */
    --fg-color:           #ffffff;
    --card-bg:            #ffffff;
    --modal-bg:           #ffffff;
    --popover-bg:         #ffffff;
    --toast-bg:           #ffffff;
    --awesomebar-focus-bg:#ffffff;

    /* controls */
    --control-bg:         #f5f7fa;
    --control-bg-on-gray: #eeeff3;
    --input-disabled-bg:  #e9ecef;

    /* button */
    --btn-default-bg:       #f5f7fa;
    --btn-default-hover-bg: #eaecf0;
    --btn-ghost-hover-bg:   rgba(0,0,0,0.06);

    /* borders */
    --border-primary:     {p};
    --border-color:       #e2e6ea;
    --dark-border-color:  #ced4da;
    --table-border-color: #e2e6ea;

    /* text */
    --text-color:         {tx};
    --text-muted:         #6c757d;

    /* focus ring */
    --highlight-shadow:   1px 1px 10px {p}33, 0px 0px 4px {p};
    --checkbox-gradient:  linear-gradient(180deg, {p} -124.51%, {p} 100%);
    --checkbox-focus-shadow: 0 0 0 2px {p}44;

    /* scrollbar */
    --scrollbar-thumb-color: {p}88;
    --scrollbar-track-color: {bg};

    /* shadows */
    --card-shadow:  0 2px 8px rgba(0,0,0,0.08);
    --modal-shadow: 0 12px 40px rgba(0,0,0,0.18);
}}

/* ================================================================
   2. NAVBAR / TOP BAR
   ================================================================ */
.navbar,
.desk-navbar {{
    background: linear-gradient(135deg, {s} 0%, {p} 100%) !important;
    border-bottom: none !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.20) !important;
}}
.navbar *,
.navbar .btn,
.navbar .nav-link,
.navbar .search-bar input,
.navbar .form-control,
.navbar .awesomplete input,
.navbar-expand .navbar-nav a {{
    color: rgba(255,255,255,0.92) !important;
}}
.navbar .search-bar,
.navbar .awesomplete {{
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: {r_sm} !important;
}}
.navbar .search-bar .form-control,
.navbar .awesomplete input {{
    background: transparent !important;
    border: none !important;
}}

/* ================================================================
   3. LEFT SIDEBAR
   ================================================================ */
.layout-side-section,
.desk-sidebar-wrapper,
.desk-sidebar,
.sidebar-column {{
    background-color: {sb} !important;
    border-right: none !important;
}}
.sidebar-item,
.sidebar-item a,
.sidebar-label,
.desk-sidebar .standard-sidebar-item span,
.sidebar-section-head {{
    color: rgba(255,255,255,0.75) !important;
}}
.standard-sidebar-item:hover,
.sidebar-item:hover {{
    background: rgba(255,255,255,0.10) !important;
    border-left: 3px solid {p} !important;
}}
.standard-sidebar-item.selected,
.sidebar-item.active {{
    background: rgba(255,255,255,0.16) !important;
    border-left: 3px solid {p} !important;
    font-weight: 600 !important;
}}
.standard-sidebar-item.selected span,
.sidebar-item.active a {{
    color: #fff !important;
}}

/* ================================================================
   4. PAGE / BODY BACKGROUND
   ================================================================ */
.page-container,
.main-section,
.layout-main,
.desk-body,
.page-content,
body {{
    background-color: {bg} !important;
}}

/* ================================================================
   5. FORM VIEWS
   ================================================================ */
.frappe-doc-section,
.form-section,
.section-body,
.page-form,
.form-page {{
    background: #fff !important;
    border-radius: {r} !important;
    border: 1px solid rgba(0,0,0,0.07) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,{'0.07 !important' if modern else '0'}) !important;
    padding: 14px 16px !important;
    margin-bottom: 10px !important;
}}
.section-head,
.form-section-heading,
.section-title {{
    color: {s} !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    border-bottom: 2px solid {p}33 !important;
    padding-bottom: 6px !important;
    margin-bottom: 12px !important;
}}
.control-label,
.frappe-control label {{
    color: {tx} !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
}}

/* Input controls */
.form-control,
.frappe-control .form-control,
.input-with-feedback,
.like-disabled-input {{
    border: 1.5px solid #dde2e8 !important;
    border-radius: {r_sm} !important;
    background: #f9fafb !important;
    color: {tx} !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.form-control:focus,
.frappe-control .form-control:focus {{
    border-color: {p} !important;
    box-shadow: 0 0 0 3px {p}22 !important;
    background: #fff !important;
    outline: none !important;
}}

/* ================================================================
   6. BUTTONS
   ================================================================ */
.btn-primary {{
    background: {p} !important;
    background: linear-gradient(135deg, {p} 0%, {s} 100%) !important;
    border-color: transparent !important;
    border-radius: {r_sm} !important;
    color: #fff !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px {p}55 !important;
    transition: transform 0.15s, box-shadow 0.2s !important;
}}
.btn-primary:hover, .btn-primary:focus {{
    background: linear-gradient(135deg, {p} 30%, {s} 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px {p}66 !important;
    color: #fff !important;
}}
.btn-default,
.btn-secondary {{
    background: #fff !important;
    border: 1.5px solid {p} !important;
    color: {p} !important;
    border-radius: {r_sm} !important;
    font-weight: 500 !important;
}}
.btn-default:hover, .btn-secondary:hover {{
    background: {p}11 !important;
    border-color: {p} !important;
}}

/* ================================================================
   7. LIST VIEWS
   ================================================================ */
.list-row,
.list-item-container {{
    background: #fff !important;
    border-radius: {r_sm} !important;
    border: 1px solid rgba(0,0,0,0.05) !important;
    box-shadow: {'0 1px 4px rgba(0,0,0,0.06)' if modern else 'none'} !important;
    transition: background 0.15s ease !important;
}}
.list-row:hover, .list-item-container:hover {{
    background: {p}0D !important;
    transform: {'translateX(2px)' if modern else 'none'} !important;
}}
.list-row-head {{
    background: {s}0D !important;
    color: {s} !important;
    font-weight: 600 !important;
    border-bottom: 2px solid {p}33 !important;
}}
.list-subject a,
.list-row .subject-col a {{
    color: {p} !important;
    font-weight: 500 !important;
}}

/* ================================================================
   8. DATA TABLE (Grid / Report)
   ================================================================ */
.dt-header .dt-cell--header,
.datatable .dt-header-row th {{
    background: {s} !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.4px !important;
}}
.datatable .dt-row:hover .dt-cell {{
    background: {p}0D !important;
}}
.dt-cell {{ border-color: rgba(0,0,0,0.05) !important; }}

/* ================================================================
   9. MODAL / DIALOG
   ================================================================ */
.modal-content {{
    border-radius: {r_lg} !important;
    border: none !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.18) !important;
    overflow: hidden !important;
}}
.modal-header {{
    background: linear-gradient(135deg, {s} 0%, {p} 100%) !important;
    color: #fff !important;
    border-bottom: none !important;
    padding: 16px 22px !important;
}}
.modal-header .modal-title,
.modal-header h4,
.modal-header h5 {{
    color: #fff !important;
    font-weight: 700 !important;
}}
.modal-header .btn-close,
.modal-header .close {{
    color: rgba(255,255,255,0.8) !important;
    filter: brightness(100) !important;
}}
.modal-body {{ padding: 22px !important; }}
.modal-footer {{
    border-top: 1px solid rgba(0,0,0,0.06) !important;
    padding: 14px 22px !important;
    background: #fafbfc !important;
}}

/* ================================================================
   10. TABS
   ================================================================ */
.nav-tabs .nav-link.active,
.form-tabs-list .nav-link.active {{
    color: {p} !important;
    border-bottom: 3px solid {p} !important;
    font-weight: 600 !important;
    background: transparent !important;
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
}}
.nav-tabs .nav-link:hover {{
    color: {p} !important;
}}

/* ================================================================
   11. PAGE TITLE / BREADCRUMBS
   ================================================================ */
.title-text, .page-title {{ color: {s} !important; font-weight: 700 !important; }}
.breadcrumb-item a {{ color: {p} !important; }}
.page-head {{ border-bottom: 1px solid rgba(0,0,0,0.07) !important; }}

/* ================================================================
   12. WORKSPACE / DASHBOARD CARDS
   ================================================================ */
.widget,
.shortcut-widget-box,
.dashboard-widget-box,
.onboarding-widget-box,
.frappe-card {{
    background: #fff !important;
    border-radius: {r} !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
    box-shadow: {'0 4px 16px rgba(0,0,0,0.07)' if modern else '0 1px 3px rgba(0,0,0,0.07)'} !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
.widget:hover, .shortcut-widget-box:hover {{
    transform: {'translateY(-3px)' if modern else 'none'} !important;
    box-shadow: {'0 12px 28px rgba(0,0,0,0.12)' if modern else '0 3px 8px rgba(0,0,0,0.10)'} !important;
}}
.widget-head .widget-title {{ font-weight: 600 !important; color: {s} !important; }}
.shortcut-widget-box .widget-title {{ color: {p} !important; }}

/* ================================================================
   13. INDICATOR PILLS / BADGES
   ================================================================ */
.indicator-pill {{ border-radius: 20px !important; font-weight: 500 !important; }}

/* ================================================================
   14. INDICATOR / LINK COLOURS
   ================================================================ */
a, .help-box a {{ color: {p} !important; }}

/* ================================================================
   15. REPORT CONTAINER
   ================================================================ */
.report-summary-wrapper,
.chart-container {{
    background: #fff !important;
    border-radius: {r} !important;
    box-shadow: {'0 4px 16px rgba(0,0,0,0.07)' if modern else 'none'} !important;
    padding: 16px !important;
}}

/* ================================================================
   16. SCROLLBARS
   ================================================================ */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {p}66; border-radius: 8px; }}
::-webkit-scrollbar-thumb:hover {{ background: {p}; }}
"""

    return css


# ──────────────────────────────────────────────────────────────────────────────
#  Login page CSS
# ──────────────────────────────────────────────────────────────────────────────
@frappe.whitelist(allow_guest=True)
def get_login_page_css():
    """Returns branded CSS specifically for the Frappe login page."""
    if not frappe.db.exists("LSERP Theme Settings", "LSERP Theme Settings"):
        return ""

    theme = frappe.get_doc("LSERP Theme Settings", "LSERP Theme Settings")
    p     = theme.primary_color   or "#078586"
    s     = theme.secondary_color or "#282f3b"
    font  = getattr(theme, "font_family", "Inter") or "Inter"
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
    background: linear-gradient(135deg, {s} 0%, {p} 100%) !important;
    min-height: 100vh;
}}
.login-content, .page-card {{
    background: #fff !important;
    border-radius: 20px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.22) !important;
    padding: 40px !important;
    border: none !important;
}}
.login-content h2, .page-card h2, .page-card h3 {{
    color: {s} !important;
    font-weight: 700 !important;
}}
.login-content .btn-primary, .page-card .btn-primary {{
    background: linear-gradient(135deg, {p} 0%, {s} 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    width: 100% !important;
    padding: 11px 20px !important;
    box-shadow: 0 4px 12px {p}44 !important;
}}
.login-content .btn-primary:hover, .page-card .btn-primary:hover {{
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}}
.login-content .form-control, .page-card .form-control {{
    border-radius: 8px !important;
    border: 1.5px solid #dde2e8 !important;
}}
.login-content .form-control:focus, .page-card .form-control:focus {{
    border-color: {p} !important;
    box-shadow: 0 0 0 3px {p}22 !important;
}}
.login-content a, .page-card a {{ color: {p} !important; }}
"""
