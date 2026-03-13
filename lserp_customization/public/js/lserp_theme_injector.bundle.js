frappe.provide('lserp_customization.theme');

$(document).ready(function() {
    lserp_customization.theme.apply_theme();
    lserp_customization.theme.apply_branding();
    lserp_customization.theme.apply_login_theme();
});

// ─────────────────────────────────────────────────────────────
//  1.  Theme CSS  (colors + optional glassmorphism)
// ─────────────────────────────────────────────────────────────
lserp_customization.theme.apply_theme = function() {
    frappe.call({
        method: "lserp_customization.api.get_theme_css",
        callback: function(r) {
            if (r.message) {
                $("<style id='lserp-custom-theme'>")
                    .prop("type", "text/css")
                    .html(r.message)
                    .appendTo("head");
                console.log("[LSERP] Dynamic theme applied.");
            }
        }
    });
};

// ─────────────────────────────────────────────────────────────
//  2.  Branding overrides  (brand name + logo replacement)
// ─────────────────────────────────────────────────────────────
lserp_customization.theme.apply_branding = function() {
    if (!frappe.boot || !frappe.boot.lserp_theme) return;

    const brand_name = frappe.boot.lserp_theme.brand_name;
    const brand_logo = frappe.boot.lserp_theme.brand_logo;

    if (brand_name) {
        // Override page title & Frappe boot info
        frappe.boot.app_name = brand_name;
        document.title = brand_name;

        // Use a MutationObserver so we catch dynamically rendered bits (v16 Vue)
        const titleObserver = new MutationObserver(function() {
            lserp_customization.theme._replace_text(brand_name, brand_logo);
        });
        titleObserver.observe(document.body, { childList: true, subtree: true });

        // Also run immediately and once after short delay
        lserp_customization.theme._replace_text(brand_name, brand_logo);
        setTimeout(function() {
            lserp_customization.theme._replace_text(brand_name, brand_logo);
        }, 1200);
    }

    if (brand_logo) {
        frappe.boot.app_logo_url = brand_logo;
        setTimeout(function() {
            lserp_customization.theme._replace_logo(brand_logo);
        }, 800);
    }
};

// ─────────────────────────────────────────────────────────────
//  3.  Helper: replace text nodes
// ─────────────────────────────────────────────────────────────
lserp_customization.theme._replace_text = function(brand_name, brand_logo) {
    const targets = [
        '.navbar-brand .app-logo',
        '.navbar-brand .app-logo-text',
        '.app-logo-text',
        '.sidebar-brand-text',
        '.workspace-title',
        '.page-title h1',
        '.desktop-app-name',
        '.page-head .title-area h3',
    ];

    targets.forEach(function(sel) {
        $(sel).each(function() {
            const el = $(this);
            if (el.text().match(/ERPNext|Frappe/i)) {
                el.text(el.text().replace(/ERPNext|Frappe/ig, brand_name));
            }
        });
    });

    $('[title="ERPNext"], [title="Frappe"]').attr('title', brand_name);

    if (document.title.match(/ERPNext|Frappe/i)) {
        document.title = document.title.replace(/ERPNext|Frappe/ig, brand_name);
    }

    if (brand_logo) {
        lserp_customization.theme._replace_logo(brand_logo);
    }
};

// ─────────────────────────────────────────────────────────────
//  4.  Helper: replace logo images
// ─────────────────────────────────────────────────────────────
lserp_customization.theme._replace_logo = function(brand_logo) {
    const logo_selectors = [
        '.navbar-brand img',
        '.app-logo img',
        '.navbar img.app-logo',
        '.workspace-logo img',
        '.desk-navbar img',
        'img.app-logo',
    ];
    logo_selectors.forEach(function(sel) {
        $(sel).attr('src', brand_logo);
    });
};
