import frappe
from frappe import _

def execute(filters=None):
    # Log execution details
    frappe.log(f"Executing Customer Fitness Journey report. User: {frappe.session.user}, Filters: {filters}, Roles: {frappe.get_roles()}")

    # Validate user permissions
    user_roles = frappe.get_roles()
    if not any(role in ["Gym Member", "Gym Admin", "Gym Trainer"] for role in user_roles):
        frappe.log(f"Permission denied for user {frappe.session.user}")
        frappe.throw(_("You do not have permission to access this report"), frappe.PermissionError)

    # Get filter values
    gym_member = filters.get("gym_member") if filters else None
    user_email = frappe.session.user

    # Define columns
    columns = [
        {"fieldname": "log_date", "label": _("Log Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "member_name", "label": _("Member Name"), "fieldtype": "Data", "width": 150},
        {"fieldname": "weight", "label": _("Weight (kg)"), "fieldtype": "Float", "width": 100},
        {"fieldname": "calories", "label": _("Calories Burned (kcal)"), "fieldtype": "Float", "width": 150}
    ]

    # Handle Gym Member role
    if "Gym Member" in user_roles and "Gym Admin" not in user_roles and "Gym Trainer" not in user_roles:
        member = frappe.get_all("Gym Member", filters={"email": user_email}, fields=["name", "full_name"], limit=1)
        if not member:
            frappe.log(f"No Gym Member profile found for user: {user_email}")
            return columns, [], "No Gym Member profile found for this user", None
        gym_member = member[0].name
        member_name = member[0].full_name
    # Handle Gym Trainer role
    elif "Gym Trainer" in user_roles and "Gym Admin" not in user_roles:
        trainer = frappe.get_all("Gym Trainer", filters={"email": user_email}, fields=["name"], limit=1)
        if not trainer:
            frappe.log(f"No Gym Trainer profile found for user: {user_email}")
            return columns, [], "No Gym Trainer profile found for this user", None
        subscriptions = frappe.get_all(
            "Gym Trainer Subscription",
            filters={"trainer": trainer[0].name, "status": "Active"},
            fields=["gym_member"],
        )
        allowed_members = [s.gym_member for s in subscriptions]
        if not allowed_members:
            frappe.log(f"No active subscriptions found for trainer: {user_email}")
            return columns, [], "No active trainees found", None
        if gym_member and gym_member not in allowed_members:
            frappe.log(f"Trainer {user_email} attempted to access unauthorized member: {gym_member}")
            frappe.throw(_("You can only view fitness logs of your trainees"), frappe.PermissionError)
        if not gym_member:
            gym_member = allowed_members[0]
        member_name = frappe.get_value("Gym Member", gym_member, "full_name")
    # Handle Gym Admin role
    else:
        if not gym_member:
            frappe.log("No Gym Member selected in filters for Gym Admin")
            return columns, [], "Please select a Gym Member", None
        member_name = frappe.get_value("Gym Member", gym_member, "full_name") or "Selected Member"

    # Log selected member
    frappe.log(f"Selected gym_member: {gym_member}, member_name: {member_name}")

    # Get fitness logs, exclude null or zero weight
    logs = frappe.get_all(
        "Gym Fitness Log",
        filters={"gym_member": gym_member, "weight": [">", 0]},
        fields=["log_date", "weight", "calories", "member_name"],
        order_by="log_date asc"
    )

    # Log retrieved logs
    frappe.log(f"Retrieved {len(logs)} fitness logs for gym_member: {gym_member}, Weights: {[log.weight for log in logs]}")

    # Prepare chart
    chart = None
    if logs:
        chart = {
            "chartType": "line",
            "data": {
                "labels": [log.log_date.strftime("%Y-%m-%d") for log in logs],
                "datasets": [
                    {
                        "name": "Weight (kg)",
                        "values": [float(log.weight) for log in logs],  # Ensure float values
                        "chartType": "line",
                        "borderColor": "#FF5733",
                        "backgroundColor": "#FF5733",
                        "tension": 0.1
                    }
                ]
            },
            "title": f"Weight Log for {member_name}",
            "axisOptions": {
                "xAxisLabel": "Date",
                "yAxisLabel": "Weight (kg)",
                "xIsSeries": True
            },
            "lineOptions": {
                "hideDots": 0,
                "dotSize": 4
            },
            
        }

    # Return with message if no logs
    if not logs:
        frappe.log(f"No valid fitness logs found for gym_member: {gym_member}")
        return columns, [], "No valid fitness logs found for the selected member", None

    return columns, logs, None, chart