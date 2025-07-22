import frappe
from frappe import _
from frappe.utils import getdate, nowdate

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if "Gym Member" not in frappe.get_roles():
        frappe.throw(_("You do not have permission to access this page"), frappe.PermissionError)
    user_email = frappe.session.user
    gym_member = frappe.get_all(
        "Gym Member",
        filters={"email": user_email},
        fields=["name", "full_name", "date_of_birth", "phone_number", "email"],
        limit=1
    )
    if not gym_member:
        context.gym_member = {
            "full_name": "Guest User",
            "date_of_birth": "",
            "phone_number": "",
            "email": user_email
        }
        context.memberships = []
        context.class_bookings = []
        context.trainer_subscriptions = []
        context.workout_plans = []
        context.fitness_logs = []
        context.message = _("No Gym Member profile found. Please contact the administrator.")
    else:
        gym_member = gym_member[0]
        memberships = frappe.get_all(
            "Gym Membership",
            filters={"gym_member": gym_member.name, "status": "Active"},
            fields=["membership_type", "start_date", "end_date"]
        )
        class_bookings = frappe.get_all(
            "Gym Class Booking",
            filters={"gym_member": gym_member.name, "booking_date": [">=", nowdate()]},
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
        fitness_logs = frappe.get_all(
            "Gym Fitness Log",
            filters={"gym_member": gym_member.name},
            fields=["log_date", "weight", "calories"],
            order_by="log_date asc"
        )
        context.gym_member = gym_member
        context.memberships = memberships
        context.class_bookings = class_bookings
        context.trainer_subscriptions = trainer_subscriptions
        context.workout_plans = workout_plans
        context.fitness_logs = fitness_logs
    context.no_header = False
    context.title = _("My Gym Profile")
    return context