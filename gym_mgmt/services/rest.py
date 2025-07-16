# gym_mgmt/api/rest.py

import frappe
from frappe.utils import nowdate, now_time


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


def update_locker_booking_status():
    today = nowdate()
    time_now = now_time()

    bookings = frappe.get_all("Gym Locker Booking", fields=["name", "booking_date", "end_time", "status"])

    for b in bookings:
        if b.status == "Cancelled":
            continue

        if b.booking_date < today:
            new_status = "Expired"
        elif b.booking_date == today and b.end_time and time_now > b.end_time:
            new_status = "Expired"
        else:
            new_status = "Active"

        frappe.db.set_value("Gym Locker Booking", b.name, "status", new_status)

def update_class_booking_status():
    today = nowdate()
    time_now = now_time()

    bookings = frappe.get_all("Gym Class Booking", fields=["name", "class_date", "end_time", "status"])

    for b in bookings:
        if b.status in ["Cancelled", "Attended"]:
            continue

        if b.class_date < today:
            new_status = "Missed"
        elif b.class_date == today and b.end_time and time_now > b.end_time:
            new_status = "Missed"
        else:
            new_status = "Booked"

        frappe.db.set_value("Gym Class Booking", b.name, "status", new_status)
