# Copyright (c) 2025, Esther Mamai and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    user_email = frappe.session.user
    if "Gym Member" not in frappe.get_roles():
        frappe.throw(_("You do not have permission to access this report"), frappe.PermissionError)

    gym_member = frappe.get_all(
        "Gym Member",
        filters={"email": user_email},
        fields=["name", "full_name", "date_of_birth", "phone_number", "email"],
        limit=1
    )
    if not gym_member:
        return [], [{"message": _("No Gym Member profile found for this user")}]

    gym_member = gym_member[0]
    memberships = frappe.get_all(
        "Gym Membership",
        filters={"gym_member": gym_member.name, "status": "Active"},
        fields=["membership_type", "start_date", "end_date"]
    )
    class_bookings = frappe.get_all(
        "Gym Class Booking",
        filters={"gym_member": gym_member.name},
        fields=["class_name", "booking_date", "status"],
        order_by="booking_date asc"
    )
    trainer_subscriptions = frappe.get_all(
        "Gym Trainer Subscription",
        filters={"gym_member": gym_member.name, "status": "Active"},
        fields=["trainer_name", "start_date", "end_date"]
    )
    workout_plans = frappe.get_all(
        "Gym Workout Plan",
        filters={"gym_member": gym_member.name},
        fields=["plan_name", "level", "published"],
        order_by="creation desc"
    )

    columns = [
        {"fieldname": "section", "label": _("Section"), "fieldtype": "Data", "width": 200},
        {"fieldname": "value", "label": _("Value"), "fieldtype": "Data", "width": 300}
    ]
    data = [
        {"section": "Full Name", "value": gym_member.full_name},
        {"section": "Email", "value": gym_member.email},
        {"section": "Date of Birth", "value": gym_member.date_of_birth},
        {"section": "Phone Number", "value": gym_member.phone_number},
        {"section": "Memberships", "value": "<br>".join([f"{m.membership_type}: {m.start_date} to {m.end_date}" for m in memberships]) or "None"},
        {"section": "Class Bookings", "value": "<br>".join([f"{c.class_name}: {c.booking_date} ({c.status})" for c in class_bookings]) or "None"},
        {"section": "Trainer Subscriptions", "value": "<br>".join([f"{t.trainer_name}: {t.start_date} to {t.end_date}" for t in trainer_subscriptions]) or "None"},
        {"section": "Workout Plans", "value": "<br>".join([f"{w.plan_name}: {w.level} ({'Published' if w.published else 'Draft'})" for w in workout_plans]) or "None"}
    ]

    return columns, data