// frappe.ready(function() {
//     if (frappe.session.user !== "Guest") {
//         frappe.call({
//             method: "redirect_after_login",
//             callback: function(r) {
//                 if (r.message && r.message.redirect_to) {
//                     window.location.href = r.message.redirect_to;
//                 } else {
//                     window.location.href = "/home";
//                 }
//             },
//             error: function() {
//                 window.location.href = "/home";
//             }
//         });
//     }
// // });

frappe.ready(function() {
    console.log("login_redirect.js loaded");
    if (frappe.session.user !== "Guest") {
        console.log("User logged in:", frappe.session.user);
    }
});