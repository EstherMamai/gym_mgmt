frappe.query_reports["Member Fitness Journey"] = {
    "filters": [
        {
            "fieldname": "gym_member",
            "label": __("Gym Member"),
            "fieldtype": "Link",
            "options": "Gym Member",
            "reqd": 1,
            "get_query": function() {
                var user_roles = frappe.user_roles;
                console.log("User roles:", user_roles, "User:", frappe.session.user);
                if (user_roles.includes("Gym Member") && !user_roles.includes("Gym Admin") && !user_roles.includes("Gym Trainer")) {
                    console.log("Restricting Gym Member filter to:", frappe.session.user);
                    return {
                        filters: {
                            "email": frappe.session.user
                        }
                    };
                } else if (user_roles.includes("Gym Trainer") && !user_roles.includes("Gym Admin")) {
                    console.log("Restricting Gym Trainer filter to trainees for:", frappe.session.user);
                    return {
                        query: "gym_mgmt.api.get_trainer_members",
                        filters: {
                            "trainer_email": frappe.session.user
                        }
                    };
                }
                console.log("Gym Admin: Allowing selection of any Gym Member");
                return {
                    doctype: "Gym Member"
                };
            }
        }
    ],
    "onload": function(report) {
        console.log("Report loaded with filters:", report.get_values());
        report.page.set_primary_action("Refresh", function() {
            report.refresh();
            console.log("Report refreshed with filters:", report.get_values());
        });
        if (!report.filters || !report.filters.length) {
            console.error("No filters rendered for Customer Fitness Journey report");
        } else {
            console.log("Filters rendered:", report.filters.map(f => f.fieldname));
        }
        // Debug chart rendering
        report.bind("report_loaded", function() {
            console.log("Report data loaded:", report.data, "Chart:", report.chart);
        });
    }
};