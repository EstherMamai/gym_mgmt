import frappe
from frappe import _

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if "Gym Admin" not in frappe.get_roles():
        frappe.throw(_("You do not have permission to access this page"), frappe.PermissionError)
    context.title = _("Gym Admin Dashboard")
    context.message = "Welcome to the Gym Admin Dashboard. Manage memberships, classes, and trainers here."
    return context