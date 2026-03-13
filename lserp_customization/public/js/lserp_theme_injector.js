frappe.provide('lserp_customization.theme');

$(document).ready(function() {
    lserp_customization.theme.apply_theme();
    lserp_customization.theme.apply_branding();
});

lserp_customization.theme.apply_theme = function() {
    frappe.call({
        method: "lserp_customization.api.get_theme_css",
        callback: function(r) {
            if(r.message) {
                var css = r.message;
                $("<style>")
                    .prop("type", "text/css")
                    .html(css)
                    .appendTo("head");
                console.log("LSERP Dynamic Theme Applied");
            }
        }
    });
};

lserp_customization.theme.apply_branding = function() {
    if (frappe.boot && frappe.boot.lserp_theme) {
        let brand_name = frappe.boot.lserp_theme.brand_name;
        let brand_logo = frappe.boot.lserp_theme.brand_logo;

        if (brand_name) {
            // Change standard app names
            frappe.boot.app_name = brand_name;
            document.title = brand_name;
            
            // Periodically check and replace UI text since Frappe renders dynamically
            setInterval(function() {
                // Change Navbar Brand
                $('.navbar-brand .app-logo, .navbar-brand .app-logo-text, .app-logo-text').text(brand_name);
                // Try grabbing elements with title=ERPNext
                $('[title="ERPNext"]').attr('title', brand_name);
            }, 500);
        }

        if (brand_logo) {
            frappe.boot.app_logo_url = brand_logo;
            setInterval(function() {
                $('.navbar-brand img, .app-logo img, .navbar-brand .app-logo-url img').attr('src', brand_logo);
            }, 500);
        }
    }
};
