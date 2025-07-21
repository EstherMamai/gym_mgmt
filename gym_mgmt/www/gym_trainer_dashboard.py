import frappe
from frappe import _

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if "Gym Trainer" not in frappe.get_roles():
        frappe.throw(_("You do not have permission to access this page"), frappe.PermissionError)
    context.title = _("Gym Trainer Dashboard")
    context.message = "Welcome to the Gym Trainer Dashboard. Manage your trainees and workout plans here."
    return context