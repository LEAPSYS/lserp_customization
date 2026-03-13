frappe.ui.form.on('LSERP Theme Settings', {
    refresh: function(frm) {
        frm.add_custom_button(__('Extract Colors from URL'), function() {
            if (!frm.doc.website_url) {
                frappe.msgprint(__('Please provide a valid Website URL before extracting.'));
                return;
            }
            frappe.call({
                method: "lserp_customization.lserp_customization.doctype.lserp_theme_settings.lserp_theme_settings.extract_colors_from_url",
                doc: frm.doc,
                callback: function(r) {
                    if(!r.exc) {
                        frm.refresh_fields();
                    }
                }
            });
        });
    },
    active_theme: function(frm) {
        if (["LS Theme", "Enummo Theme"].includes(frm.doc.active_theme)) {
            frm.save();
        }
    }
});
