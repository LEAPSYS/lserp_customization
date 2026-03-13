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
                console.log("[LSERP] Dynamic theme CSS applied.");
            }
        }
    });
};

// ─────────────────────────────────────────────────────────────
//  2.  Branding overrides  (brand name + sidebar/navbar logo)
// ─────────────────────────────────────────────────────────────
lserp_customization.theme.apply_branding = function() {
    if (!frappe.boot || !frappe.boot.lserp_theme) return;

    const brand_name = frappe.boot.lserp_theme.brand_name;
    const brand_logo = frappe.boot.lserp_theme.brand_logo;

    if (brand_name || brand_logo) {
        // Set basic Frappe boot properties
        if (brand_name) {
            frappe.boot.app_name = brand_name;
            document.title = brand_name;
        }
        if (brand_logo) frappe.boot.app_logo_url = brand_logo;

        // Use a MutationObserver to catch dynamic page loads (Vue routing, dialogs, etc.)
        const domObserver = new MutationObserver(function(mutations) {
            lserp_customization.theme._inject_sidebar_branding(brand_name, brand_logo);
            lserp_customization.theme._replace_logo(brand_logo);
            if (brand_name) {
                lserp_customization.theme._walk_and_replace_text(document.body, brand_name);
                lserp_customization.theme._replace_titles(brand_name);
            }
        });
        domObserver.observe(document.body, { childList: true, subtree: true });

        // Run immediately on first load
        lserp_customization.theme._inject_sidebar_branding(brand_name, brand_logo);
        lserp_customization.theme._replace_logo(brand_logo);
        if (brand_name) {
            lserp_customization.theme._walk_and_replace_text(document.body, brand_name);
            lserp_customization.theme._replace_titles(brand_name);
        }
    }
};

// ─────────────────────────────────────────────────────────────
//  3.  Inject Branding Header into Sidebar
// ─────────────────────────────────────────────────────────────
lserp_customization.theme._inject_sidebar_branding = function(brand_name, brand_logo) {
    // 1. Target the Frappe V15 native App Switcher (Sidebar Dropdown)
    const $switcher = $('.sidebar-item-wrapper.dropdown .sidebar-toggle-btn');
    if ($switcher.length > 0) {
        if (brand_logo) {
            // Replace the default squircle SVG with our exact img
            const $iconContainer = $switcher.find('.sidebar-item-icon');
            if ($iconContainer.length > 0 && $iconContainer.find('img.custom-app-logo').length === 0) {
                $iconContainer.empty().css({
                    'background': 'transparent',
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center',
                    'padding': '0',
                    'border-radius': '0'
                });
                $iconContainer.append(`<img class="custom-app-logo" src="${brand_logo}" style="width: 100%; height: 100%; object-fit: contain;">`);
            }
        }

        if (brand_name) {
            const $brandText = $switcher.find('.sidebar-brand-text');
            if ($brandText.length > 0 && !$brandText.data('lserp-fixed')) {
                $brandText.text(brand_name).css({
                    'font-size': '12px',
                    'font-weight': '700',
                    'opacity': '1',
                    'color': 'var(--primary-color)'
                });
                $brandText.data('lserp-fixed', true);
            }
        }
    }

    // 2. Remove previously injected separate brand header block if any
    if ($('.lserp-sidebar-brand').length > 0) {
        $('.lserp-sidebar-brand').remove();
    }
};

// ─────────────────────────────────────────────────────────────
//  4.  Aggressive DOM Text Walker (replaces ERPNext completely)
// ─────────────────────────────────────────────────────────────
lserp_customization.theme._walk_and_replace_text = function(node, brand_name) {
    // Skip script/style tags or already processed custom brand strings (to avoid infinite loops)
    if (node.nodeType === 1 && (node.nodeName === 'SCRIPT' || node.nodeName === 'STYLE')) {
        return;
    }

    if (node.nodeType === 3) { // Text Node
        let val = node.nodeValue;
        if (val && /ERPNext|Frappe/i.test(val)) {
            // Check if it's purely our brand name so we don't end up with BrandNameNext etc
            node.nodeValue = val.replace(/ERPNext|Frappe/ig, brand_name);
        }
    } else {
        // Recurse down children
        for (let i = 0; i < node.childNodes.length; i++) {
            lserp_customization.theme._walk_and_replace_text(node.childNodes[i], brand_name);
        }
    }
};

// ─────────────────────────────────────────────────────────────
//  5.  Replace Attributes (Titles, Placeholders)
// ─────────────────────────────────────────────────────────────
lserp_customization.theme._replace_titles = function(brand_name) {
    // Replace hover tooltips
    $('[title*="ERPNext"], [title*="Frappe"]').each(function() {
        const t = $(this).attr('title');
        $(this).attr('title', t.replace(/ERPNext|Frappe/ig, brand_name));
    });
    
    // Replace inputs holding defaults
    $('[placeholder*="ERPNext"], [placeholder*="Frappe"]').each(function() {
        const p = $(this).attr('placeholder');
        $(this).attr('placeholder', p.replace(/ERPNext|Frappe/ig, brand_name));
    });

    // Fix page title tag
    if (document.title.match(/ERPNext|Frappe/i)) {
        document.title = document.title.replace(/ERPNext|Frappe/ig, brand_name);
    }
};

// ─────────────────────────────────────────────────────────────
//  6.  Navbar Top-Left Logo Override
// ─────────────────────────────────────────────────────────────
lserp_customization.theme._replace_logo = function(brand_logo) {
    if (!brand_logo) return;
    
    // Force the top-left navbar logo explicitly
    const $navLogo = $('.navbar-brand img, .app-logo');
    if ($navLogo.length > 0 && $navLogo.attr('src') !== brand_logo) {
        $navLogo.attr('src', brand_logo)
                .css({'max-height': '28px', 'width': 'auto', 'object-fit': 'contain'});
    }

    // Hide any text right next to the navbar logo so it doesn't look cluttered (we have it in sidebar now)
    const $navText = $('.navbar-brand .app-logo-text, .navbar-brand .app-name');
    if ($navText.length > 0 && brand_logo) {
        $navText.hide();
    }
};

// ─────────────────────────────────────────────────────────────
//  7.  Login Page specific theme
// ─────────────────────────────────────────────────────────────
lserp_customization.theme.apply_login_theme = function() {
    if (window.location.pathname !== '/login') return;

    frappe.call({
        method: "lserp_customization.api.get_login_page_css",
        callback: function(r) {
            if (r.message) {
                $("<style id='lserp-login-theme'>")
                    .prop("type", "text/css")
                    .html(r.message)
                    .appendTo("head");
            }
        }
    });

    // On login page, hide the standard Frappe login graphic if there's a custom logo
    if (frappe.boot && frappe.boot.lserp_theme && frappe.boot.lserp_theme.brand_logo) {
        $('.login-content img').first().attr('src', frappe.boot.lserp_theme.brand_logo);
        $('.page-card-head img').first().attr('src', frappe.boot.lserp_theme.brand_logo);
    }
};
