import frappe


def _get_active_theme():
    """Returns the active LSERP Brand Theme doc, or None."""
    if not frappe.db.exists("LSERP Theme Settings", "LSERP Theme Settings"):
        return None
    active_name = frappe.db.get_single_value("LSERP Theme Settings", "active_theme")
    if not active_name:
        return None
    if not frappe.db.exists("LSERP Brand Theme", active_name):
        return None
    return frappe.get_doc("LSERP Brand Theme", active_name)


# ──────────────────────────────────────────────────────────────────────────────
#  Main desk theme CSS
# ──────────────────────────────────────────────────────────────────────────────
@frappe.whitelist(allow_guest=True)
def get_theme_css():
    """Returns full CSS for all Frappe internal pages based on active LSERP Brand Theme."""
    theme = _get_active_theme()
    if not theme:
        return ""

    p  = theme.primary_color    or "#078586"
    s  = theme.secondary_color  or "#282f3b"
    bg = theme.background_color or "#f0f3f9"
    sb = theme.sidebar_background or "#1f2530"

    modern      = bool(theme.enable_modern_dashboard)
    density     = theme.ui_density   or "Comfortable"
    navbar_style = theme.navbar_style or "Gradient"
    font        = theme.font_family   or "Inter"

    # ── Font setup ─────────────────────────────────────────────────────────────
    font_url_map = {
        "Inter":   "Inter:wght@300;400;500;600;700",
        "Outfit":  "Outfit:wght@300;400;500;600;700",
        "Roboto":  "Roboto:wght@300;400;500;700",
        "DM Sans": "DM+Sans:wght@300;400;500;600;700",
        "72":      "72:wght@400;700",  # SAP 72 font via Google Fonts fallback
    }
    font_url = font_url_map.get(font)

    # SAP 72 font isn't on Google Fonts — use it from SAP CDN or fall back to Inter
    if font == "72":
        font_import = ""  # Will use system font stack below
        font_stack  = "'72', '72Full', Arial, Helvetica, sans-serif"
    else:
        font_import = f"@import url('https://fonts.googleapis.com/css2?family={font_url}&display=swap');"
        font_stack  = f"'{font}', sans-serif"

    if density == "Compact":
        # USE THE USER-PROVIDED EXACT SAP FIORI PAYLOAD
        css = f"""
/* =====================================================
   ERPNext SAP Fiori Style Theme (User Provided Payload)
   ===================================================== */

:root {{
  --sapPrimary: {p};
  --sapPrimaryHover: {s};
  --sapBackground: #f5f6f7;
  --sapPanel: #ffffff;
  --sapBorder: #d9d9d9;
  --sapText: #32363a;
  --sapFont: {font_stack};
  --sapSuccess: #107e3e;
  --sapWarning: #e9730c;
  --sapError: #bb0000;
  
  /* Frappe Variable Overrides to match SAP */
  --primary: var(--sapPrimary);
  --btn-primary: var(--sapPrimary);
  --text-color: var(--sapText);
  --navbar-bg: #ffffff;
  --bg-color: var(--sapBackground);
  --control-bg: #fff;
  --border-color: var(--sapBorder);
  --dark-border-color: var(--sapBorder);
  --table-border-color: var(--sapBorder);
}}

/* ---------- GLOBAL ---------- */
body {{
  font-family: var(--sapFont) !important;
  background: var(--sapBackground) !important;
  color: var(--sapText) !important;
  font-size: 13px !important;
}}

.page-container {{ background: var(--sapBackground) !important; }}
.layout-main-section {{ background: transparent !important; }}

/* ---------- NAVBAR ---------- */
.navbar, .desk-navbar {{
  background: white !important;
  border-bottom: 1px solid var(--sapBorder) !important;
  height: 48px !important;
  box-shadow: none !important;
}}
.navbar .navbar-brand {{ font-weight: 600; font-size: 16px; color: var(--sapText) !important; }}
.navbar .nav-link, .navbar * {{ color: var(--sapText) !important; }}

/* ---------- SIDEBAR ---------- */
.layout-side-section, .desk-sidebar {{
  background: white !important;
  border-right: 1px solid var(--sapBorder) !important;
}}
.sidebar-item, .standard-sidebar-item {{
  padding: 8px 12px !important;
  border-radius: 4px !important;
  color: var(--sapText) !important;
}}
.sidebar-item:hover, .standard-sidebar-item:hover {{ background: #f0f6ff !important; }}
.sidebar-item.active, .standard-sidebar-item.selected {{ background: #f0f6ff !important; font-weight: 600 !important; }}

/* ---------- BUTTONS ---------- */
.btn-primary {{
  background: var(--sapPrimary) !important;
  border-color: var(--sapPrimary) !important;
  border-radius: 4px !important;
  color: #fff !important;
  box-shadow: none !important;
}}
.btn-primary:hover {{ background: var(--sapPrimaryHover) !important; }}
.btn-default, .btn-secondary {{
  background: white !important;
  border: 1px solid var(--sapBorder) !important;
  border-radius: 4px !important;
}}

/* ---------- INPUT FIELDS ---------- */
.form-control, .awesomplete input {{
  border: 1px solid var(--sapBorder) !important;
  border-radius: 4px !important;
  background: #fff !important;
}}
.form-control:focus {{
  border-color: var(--sapPrimary) !important;
  box-shadow: none !important;
}}

/* ---------- FORM SECTIONS ---------- */
.form-section, .frappe-doc-section {{
  background: var(--sapPanel) !important;
  border: 1px solid var(--sapBorder) !important;
  border-radius: 6px !important;
  padding: 16px !important;
  box-shadow: none !important;
  margin-bottom: 8px !important;
}}
.section-head, .form-section-heading {{
  font-size: 14px !important;
  font-weight: 600 !important;
  border-bottom: none !important;
  color: var(--sapText) !important;
}}
.control-label {{
  font-weight: 500 !important;
  color: #6a6d70 !important;
}}

/* ---------- TABLES ---------- */
.grid-body {{ background: white !important; }}
.grid-heading-row, .dt-header-row th {{
  background: #fafafa !important;
  border-bottom: 1px solid var(--sapBorder) !important;
  color: var(--sapText) !important;
}}
.grid-row:hover, .dt-row:hover .dt-cell {{ background: #f0f6ff !important; }}
.dt-cell {{ border-color: var(--sapBorder) !important; }}

/* ---------- LIST VIEW ---------- */
.list-row {{
  border-bottom: 1px solid var(--sapBorder) !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}}
.list-row:hover {{ background: #f0f6ff !important; }}
.list-row-head {{ background: #fafafa !important; border-bottom: 1px solid var(--sapBorder) !important; }}

/* ---------- DASHBOARD WIDGET ---------- */
.widget, .shortcut-widget-box, .frappe-card {{
  background: white !important;
  border: 1px solid var(--sapBorder) !important;
  border-radius: 6px !important;
  box-shadow: none !important;
}}
.widget-head, .widget-title {{ font-weight: 600 !important; color: var(--sapText) !important; }}

/* ---------- DIALOG WINDOWS ---------- */
.modal-content {{
  border-radius: 6px !important;
  border: 1px solid var(--sapBorder) !important;
}}
.modal-header {{
  background: #fff !important;
  border-bottom: 1px solid var(--sapBorder) !important;
  color: var(--sapText) !important;
}}
.modal-title {{ color: var(--sapText) !important; }}
.modal-header .btn-close {{ filter: none !important; color: #6a6d70 !important; }}

/* ---------- STATUS COLORS ---------- */
.indicator.green, .indicator-pill.green {{ background: var(--sapSuccess) !important; color: #fff !important; }}
.indicator.orange, .indicator-pill.orange {{ background: var(--sapWarning) !important; color: #fff !important; }}
.indicator.red, .indicator-pill.red {{ background: var(--sapError) !important; color: #fff !important; }}

/* ---------- WORKSPACE ICONS ---------- */
.workspace-icon {{ background: #f4f5f7 !important; border-radius: 6px !important; }}

/* ---------- REPORT TABLE ---------- */
.report-wrapper table {{ border: 1px solid var(--sapBorder) !important; }}
.report-wrapper th {{ background: #fafafa !important; }}

/* ---------- TAB SECTION ---------- */
.form-tabs {{ border-bottom: 1px solid var(--sapBorder) !important; }}
.form-tabs .nav-link.active {{ border-bottom: 2px solid var(--sapPrimary) !important; color: var(--sapPrimary) !important; }}

/* ---------- DROPDOWN ---------- */
.dropdown-menu {{ border: 1px solid var(--sapBorder) !important; border-radius: 4px !important; }}

/* ---------- SCROLLBAR ---------- */
::-webkit-scrollbar {{ width: 8px !important; }}
::-webkit-scrollbar-thumb {{ background: #c7c7c7 !important; border-radius: 4px !important; }}
"""
    else:
        # ── ORIGINAL / STANDARD OUTPUT BUILDER FOR NON-COMPACT ───────────────────
        
        # ── Border radius tokens ───────────────────────────────────────────────────
        if density == "Comfortable" and modern:
            r, r_sm, r_lg = "12px", "8px", "16px"
        elif density == "Comfortable":
            r, r_sm, r_lg = "6px", "4px", "8px"
        else:
            r, r_sm, r_lg = "4px", "2px", "4px"

        if density == "Ultra Compact":
            row_h   = "24px"
            inp_h   = "20px"
            pad_f   = "3px 6px"     
            pad_c   = "2px 4px"     
            fsize   = "12px"
            label_s = "10px"
            sec_pad = "6px 10px"
        else:  # Comfortable
            row_h   = "44px"
            inp_h   = "28px"
            pad_f   = "14px 16px"
            pad_c   = "5px 10px"
            fsize   = "14px"
            label_s = "12px"
            sec_pad = "14px 18px"
            
        if navbar_style == "Gradient":
            navbar_bg  = f"linear-gradient(135deg, {s} 0%, {p} 100%)"
            navbar_txt = "rgba(255,255,255,0.92)"
            navbar_shadow = "0 2px 10px rgba(0,0,0,0.18)"
            navbar_border = "none"
        elif navbar_style == "Flat":
            navbar_bg  = p
            navbar_txt = "#fff"
            navbar_shadow = f"0 1px 4px {p}44"
            navbar_border = "none"
        else:  # Minimal
            navbar_bg  = "#ffffff"
            navbar_txt = "#1a1f36"
            navbar_shadow = "none"
            navbar_border = f"1px solid #e2e6ea"

        css = f"""
/* ================================================================
   LSERP Theme: {theme.theme_name}  |  Density: {density}  |  Navbar: {navbar_style}
   ================================================================ */

/* ── 0. Font ─────────────────────────────────────────────────── */
{font_import}
html, body, input, button, select, textarea,
.form-control, .frappe-control, .btn, .sidebar-item,
.widget, .list-row, .dt-cell, .dt-header {{
    font-family: {font_stack} !important;
    font-size: {fsize} !important;
}}

/* ================================================================
   1. FRAPPE CSS TOKEN OVERRIDES
   ================================================================ */
:root,
[data-theme="light"] {{
    --primary:              {p};
    --primary-color:        {p};
    --brand-color:          {p};
    --btn-primary:          {p};
    --progress-bar-bg:      {p};
    --navbar-bg:            {s};
    --sidebar-select-color: rgba(255,255,255,0.12);
    --bg-color:             {bg};
    --subtle-accent:        {bg};
    --subtle-fg:            {bg};
    --fg-color:             #ffffff;
    --card-bg:              #ffffff;
    --modal-bg:             #ffffff;
    --popover-bg:           #ffffff;
    --toast-bg:             #ffffff;
    --awesomebar-focus-bg:  #ffffff;
    --control-bg:           #f5f7fa;
    --control-bg-on-gray:   #eeeff3;
    --input-disabled-bg:    #e9ecef;
    --btn-default-bg:       #f5f7fa;
    --btn-default-hover-bg: #eaecf0;
    --btn-ghost-hover-bg:   rgba(0,0,0,0.06);
    --border-primary:       {p};
    --border-color:         #e2e6ea;
    --dark-border-color:    #ced4da;
    --table-border-color:   #e2e6ea;
    --text-color:           #1a1f36;
    --text-muted:           #6c757d;
    --body-color:           #1a1f36;
    --input-height:         {inp_h};
    --btn-height:           {inp_h};
    --highlight-shadow:     1px 1px 10px {p}33, 0 0 4px {p};
    --checkbox-gradient:    linear-gradient(180deg, {p} -124.51%, {p} 100%);
    --checkbox-focus-shadow:0 0 0 2px {p}44;
    --scrollbar-thumb-color:{p}88;
    --scrollbar-track-color:{bg};
    --card-shadow:          0 1px 4px rgba(0,0,0,0.08);
    --list-row-height:      {row_h};
}}

/* ── 2. Navbar ───────────────────────────────────────────────── */
.navbar, .desk-navbar {{
    background: {navbar_bg} !important;
    border-bottom: {navbar_border} !important;
    box-shadow: {navbar_shadow} !important;
    min-height: 48px !important;
}}
.navbar *, .navbar .btn, .navbar .nav-link,
.navbar .search-bar input, .navbar .form-control,
.navbar .awesomplete input {{ color: {navbar_txt} !important; }}
.navbar .search-bar, .navbar .awesomplete {{
    background: {'rgba(255,255,255,0.15)' if navbar_style != 'Minimal' else '#f5f7fa'} !important;
    border: 1px solid {'rgba(255,255,255,0.3)' if navbar_style != 'Minimal' else '#dee2e6'} !important;
    border-radius: {r_sm} !important;
}}
.navbar .search-bar .form-control {{ background: transparent !important; border: none !important; }}

/* ── 3. Left Sidebar ─────────────────────────────────────────── */
.layout-side-section, .desk-sidebar-wrapper,
.desk-sidebar, .sidebar-column {{
    background-color: {sb} !important;
    border-right: none !important;
}}
.sidebar-item, .sidebar-item a, .sidebar-label,
.desk-sidebar .standard-sidebar-item span,
.sidebar-section-head {{ color: rgba(255,255,255,0.75) !important; font-size: {label_s} !important; }}
.standard-sidebar-item, .sidebar-item {{
    padding: 8px 14px !important;
    min-height: 36px !important;
}}
.standard-sidebar-item:hover, .sidebar-item:hover {{
    background: rgba(255,255,255,0.10) !important;
    border-left: 3px solid {p} !important;
}}
.standard-sidebar-item.selected, .sidebar-item.active {{
    background: rgba(255,255,255,0.16) !important;
    border-left: 3px solid {p} !important;
    font-weight: 600 !important;
}}
.standard-sidebar-item.selected span,
.sidebar-item.active a {{ color: #fff !important; }}

/* ── 4. Page Background + Body Text ─────────────────────────── */
.page-container, .main-section, .layout-main, .desk-body, .page-content, body {{
    background-color: {bg} !important;
}}
.page-container, .main-section, .layout-main, .desk-body, .page-content,
.frappe-card, .form-page, .list-row, .report-summary-wrapper {{
    color: #1a1f36 !important;
    font-size: {fsize} !important;
}}

/* ── 5. Form Views ───────────────────────────────────────────── */
.frappe-doc-section, .form-section, .section-body, .page-form, .form-page {{
    background: #fff !important;
    border-radius: {r} !important;
    border: 1px solid #e2e6ea !important;
    box-shadow: {'0 1px 4px rgba(0,0,0,0.06)' if modern else 'none'} !important;
    padding: {sec_pad} !important;
    margin-bottom: 10px !important;
}}
.section-head, .form-section-heading, .section-title {{
    color: {s} !important;
    font-weight: 600 !important;
    font-size: {label_s} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
    border-bottom: 1px solid #e2e6ea !important;
    padding-bottom: 6px !important;
    margin-bottom: 10px !important;
    background: transparent !important;
}}
.control-label, .frappe-control label {{
    color: #52606d !important;
    font-weight: 500 !important;
    font-size: {label_s} !important;
    margin-bottom: 4px !important;
}}
.form-control, .frappe-control .form-control,
.input-with-feedback, .like-disabled-input {{
    border: 1px solid #c9d1d9 !important;
    border-radius: {r_sm} !important;
    background: #fff !important;
    color: #1a1f36 !important;
    height: {inp_h} !important;
    padding: {pad_c} !important;
    font-size: {fsize} !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}}
.form-control:focus, .frappe-control .form-control:focus {{
    border-color: {p} !important;
    box-shadow: 0 0 0 2px {p}22 !important;
    background: #fff !important;
    outline: none !important;
}}
.like-disabled-input, [readonly] {{
    background: #f5f7fa !important;
    color: #6c757d !important;
}}

/* ── 6. Buttons ──────────────────────────────────────────────── */
.btn-primary {{
    background: {p} !important;
    border-color: {p} !important;
    border-radius: {r_sm} !important;
    color: #fff !important;
    font-weight: 500 !important;
    height: {inp_h} !important;
    padding: {pad_c} !important;
    font-size: {fsize} !important;
    box-shadow: 0 2px 6px {p}44 !important;
    transition: background 0.15s, box-shadow 0.15s !important;
}}
.btn-primary:hover, .btn-primary:focus {{
    background: {s} !important;
    border-color: {s} !important;
    color: #fff !important;
    box-shadow: 0 4px 12px {p}55 !important;
}}
.btn-default, .btn-secondary {{
    background: #fff !important;
    border: 1px solid #c9d1d9 !important;
    color: #1a1f36 !important;
    border-radius: {r_sm} !important;
    font-weight: 400 !important;
    height: {inp_h} !important;
    padding: {pad_c} !important;
    font-size: {fsize} !important;
}}
.btn-default:hover, .btn-secondary:hover {{
    background: #f0f3f7 !important;
    border-color: #a0aab4 !important;
}}

/* ── 7. List Views ───────────────────────────────────────────── */
.list-row, .list-item-container {{
    background: #fff !important;
    border-radius: 0 !important;
    border-bottom: 1px solid #e9ecef !important;
    box-shadow: none !important;
    min-height: {row_h} !important;
    padding: 8px 14px !important;
    transition: background 0.1s ease !important;
}}
.list-row:hover, .list-item-container:hover {{
    background: {p}0A !important;
}}
.list-row-head {{
    background: #f5f7fa !important;
    color: #52606d !important;
    font-weight: 600 !important;
    font-size: {label_s} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    border-bottom: 2px solid #e2e6ea !important;
    min-height: {row_h} !important;
}}
.list-subject a, .list-row .subject-col a {{
    color: {p} !important;
    font-weight: 500 !important;
    font-size: {fsize} !important;
}}

/* ── 8. Data Tables ──────────────────────────────────────────── */
.dt-header .dt-cell--header, .datatable .dt-header-row th {{
    background: #f5f7fa !important;
    color: #52606d !important;
    font-weight: 600 !important;
    font-size: {label_s} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    border-bottom: 2px solid {p}44 !important;
    height: {row_h} !important;
    padding: {pad_c} !important;
}}
.dt-cell {{
    height: {row_h} !important;
    padding: {pad_c} !important;
    border-color: #e9ecef !important;
    font-size: {fsize} !important;
}}
.datatable .dt-row:hover .dt-cell {{ background: {p}08 !important; }}

/* ── 9. Modal / Dialog ───────────────────────────────────────── */
.modal-content {{
    border-radius: {r_lg} !important;
    border: 1px solid #e2e6ea !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.16) !important;
    overflow: hidden !important;
}}
.modal-header {{
    background: {'linear-gradient(135deg, ' + s + ' 0%, ' + p + ' 100%)' if navbar_style == 'Gradient' else p if navbar_style == 'Flat' else '#f5f7fa'} !important;
    color: {'#fff' if navbar_style != 'Minimal' else '#1a1f36'} !important;
    border-bottom: {'none' if navbar_style != 'Minimal' else '1px solid #e2e6ea'} !important;
    padding: 14px 20px !important;
}}
.modal-header .modal-title, .modal-header h4, .modal-header h5 {{
    color: {'#fff' if navbar_style != 'Minimal' else '#1a1f36'} !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}}
.modal-header .btn-close, .modal-header .close {{
    color: {'rgba(255,255,255,0.85)' if navbar_style != 'Minimal' else '#6c757d'} !important;
    filter: {'brightness(100)' if navbar_style != 'Minimal' else 'none'} !important;
}}
.modal-body {{ padding: 20px !important; }}
.modal-footer {{
    border-top: 1px solid #e2e6ea !important;
    padding: 12px 20px !important;
    background: #fafbfc !important;
}}

/* ── 10. Tabs ────────────────────────────────────────────────── */
.nav-tabs .nav-link {{
    padding: 8px 16px !important;
    font-size: {fsize} !important;
}}
.nav-tabs .nav-link.active, .form-tabs-list .nav-link.active {{
    color: {p} !important;
    border-bottom: 2px solid {p} !important;
    font-weight: 600 !important;
    background: transparent !important;
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
}}
.nav-tabs .nav-link:hover {{ color: {p} !important; }}

/* ── 11. Page Title / Breadcrumbs ────────────────────────────── */
.title-text, .page-title {{
    color: #1a1f36 !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}}
.breadcrumb-item a {{ color: {p} !important; font-size: {fsize} !important; }}
.page-head {{
    border-bottom: 1px solid #e2e6ea !important;
    padding: 8px 0 !important;
}}

/* ── 12. Workspace Cards ─────────────────────────────────────── */
.widget, .shortcut-widget-box, .dashboard-widget-box,
.onboarding-widget-box, .frappe-card {{
    background: #fff !important;
    border-radius: {r} !important;
    border: 1px solid #e2e6ea !important;
    box-shadow: {'0 4px 14px rgba(0,0,0,0.07)' if modern else '0 1px 3px rgba(0,0,0,0.06)'} !important;
    padding: 14px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
.widget:hover, .shortcut-widget-box:hover {{
    transform: {'translateY(-2px)' if modern else 'none'} !important;
    box-shadow: {'0 10px 24px rgba(0,0,0,0.10)' if modern else '0 2px 8px rgba(0,0,0,0.08)'} !important;
}}
.widget-head .widget-title {{
    font-weight: 600 !important;
    color: #1a1f36 !important;
    font-size: {fsize} !important;
}}
.shortcut-widget-box .widget-title {{ color: {p} !important; }}

/* ── 13. Links (light-bg areas only) ─────────────────────────── */
.page-container a:not(.btn):not(.nav-link):not(.sidebar-item),
.list-row a, .breadcrumb-item a,
.form-page a:not(.btn), .frappe-card a:not(.btn),
.widget a:not(.btn), .help-box a {{ color: {p} !important; }}

/* ── 14. Indicator Pills ─────────────────────────────────────── */
.indicator-pill {{
    border-radius: 3px !important;
    font-weight: 500 !important;
    font-size: {label_s} !important;
    padding: 2px 6px !important;
}}

/* ── 15. Reports ─────────────────────────────────────────────── */
.report-summary-wrapper, .chart-container {{
    background: #fff !important;
    border-radius: {r} !important;
    border: 1px solid #e2e6ea !important;
    box-shadow: none !important;
    padding: 16px !important;
}}

/* ── 16. Scrollbars ──────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {p}55; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: {p}; }}
"""

    brand_name = theme.brand_name or "LEAPSYS"
    brand_logo = theme.brand_logo or ""
    
    # Unbreakable CSS App Switcher Overrides
    css += f"""
/* ── Sidebar App Switcher Branding Override ── */
.sidebar-item-wrapper.dropdown .sidebar-toggle-btn .sidebar-brand-text {{
    font-size: 0 !important;
    visibility: hidden !important;
}}
.sidebar-item-wrapper.dropdown .sidebar-toggle-btn .sidebar-brand-text::after {{
    content: "{brand_name}" !important;
    visibility: visible !important;
    display: block;
    font-size: 11px !important;
    font-weight: 700 !important;
    color: {p} !important;
    text-transform: uppercase !important;
}}
"""
    if brand_logo:
        css += f"""
.sidebar-item-wrapper.dropdown .sidebar-toggle-btn .sidebar-item-icon svg {{
    display: none !important;
}}
.sidebar-item-wrapper.dropdown .sidebar-toggle-btn .sidebar-item-icon {{
    background-image: url('{brand_logo}') !important;
    background-size: contain !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-color: transparent !important;
    border-radius: 0 !important;
}}
"""

    # Append any custom CSS from the theme record
    if theme.custom_css:
        css += f"\n/* ── Custom CSS: {theme.theme_name} ── */\n{theme.custom_css}\n"

    return css


# ──────────────────────────────────────────────────────────────────────────────
#  Login page CSS
# ──────────────────────────────────────────────────────────────────────────────
@frappe.whitelist(allow_guest=True)
def get_login_page_css():
    """Returns branded CSS for the Frappe login page."""
    theme = _get_active_theme()
    if not theme:
        return ""

    p  = theme.primary_color   or "#078586"
    s  = theme.secondary_color or "#282f3b"
    ns = theme.navbar_style    or "Gradient"
    font = theme.font_family   or "Inter"

    font_url_map = {
        "Inter":   "Inter:wght@300;400;500;600;700",
        "Outfit":  "Outfit:wght@300;400;500;600;700",
        "Roboto":  "Roboto:wght@300;400;500;700",
        "DM Sans": "DM+Sans:wght@300;400;500;600;700",
    }
    font_import = ""
    font_stack  = f"'{font}', sans-serif"
    if font in font_url_map:
        font_import = f"@import url('https://fonts.googleapis.com/css2?family={font_url_map[font]}&display=swap');"
    elif font == "72":
        font_stack = "'72', '72Full', Arial, sans-serif"

    if ns == "Gradient":
        login_bg = f"linear-gradient(135deg, {s} 0%, {p} 100%)"
    elif ns == "Flat":
        login_bg = p
    else:
        login_bg = f"linear-gradient(160deg, #e8edf2 0%, #f4f5f7 100%)"

    return f"""
{font_import}
body {{
    font-family: {font_stack} !important;
    background: {login_bg} !important;
    min-height: 100vh;
}}
.login-content, .page-card {{
    background: #fff !important;
    border-radius: 8px !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.18) !important;
    padding: 36px !important;
    border: none !important;
}}
.login-content h2, .page-card h2, .page-card h3 {{
    color: #1a1f36 !important;
    font-weight: 600 !important;
    font-size: 1.15rem !important;
}}
.login-content .btn-primary, .page-card .btn-primary {{
    background: {p} !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 500 !important;
    width: 100% !important;
    padding: 10px 20px !important;
}}
.login-content .btn-primary:hover, .page-card .btn-primary:hover {{
    background: {s} !important;
}}
.login-content .form-control, .page-card .form-control {{
    border-radius: 4px !important;
    border: 1px solid #c9d1d9 !important;
    height: 32px !important;
    font-size: 13px !important;
}}
.login-content .form-control:focus, .page-card .form-control:focus {{
    border-color: {p} !important;
    box-shadow: 0 0 0 2px {p}22 !important;
}}
.login-content a, .page-card a {{ color: {p} !important; }}
"""
