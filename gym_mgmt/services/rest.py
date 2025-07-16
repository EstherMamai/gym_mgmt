# gym_mgmt/api/rest.py

import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def update_membership_status(doc, method):
    """
    Automatically sets the status of Gym Membership based on dates.
    """
    today = nowdate()

    if doc.status == "Cancelled":
        return  # Do not override Cancelled status

    if doc.end_date and today > doc.end_date:
        doc.status = "Expired"
    elif doc.start_date and doc.start_date <= today <= doc.end_date:
        doc.status = "Active"
    elif doc.start_date and today < doc.start_date:
        doc.status = "Upcoming"