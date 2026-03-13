frappe.provide('lserp_customization.theme');

$(document).ready(function() {
    lserp_customization.theme.apply_theme();
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
