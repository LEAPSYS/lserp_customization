app_name = "lserp_customization"
app_title = "LSERP Customization"
app_publisher = "LEAPSYS"
app_description = "LSERP White-label & Theme Configurator"
app_email = "info@leapsys.com"
app_license = "mit"

# ── JS injected into every Frappe desk page ───────────────────────────────────
app_include_js = "/assets/lserp_customization/js/lserp_theme_injector.bundle.js"

# ── Boot hook — injects active theme data into frappe.boot ───────────────────
extend_bootinfo = "lserp_customization.boot.extend_bootinfo"

# ── Fixtures — installed automatically on bench migrate ──────────────────────
# Seeded preset themes: Enumoo, LEAPSYS, Standard Light
fixtures = [
    {
        "doctype": "LSERP Brand Theme",
        "filters": [["is_predefined", "=", 1]]
    }
]
