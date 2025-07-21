# gym_mgmt/api/rest.py

import frappe
from frappe.utils import nowdate
from datetime import datetime
from frappe.utils.response import redirect


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


# def create_gym_member(doc, method):
#     # Check if the user has the "Gym Member" role
#     if any(role.role == "Gym Member" for role in doc.roles):
#         # Prevent duplicate Gym Member records
#         if not frappe.db.exists("Gym Member", {"email": doc.email}):
#             full_name = (
#                 doc.full_name
#                 if hasattr(doc, "full_name") and doc.full_name
#                 else f"{doc.first_name or ''} {doc.last_name or ''}".strip()
#             )

#             gym_member = frappe.get_doc({
#                 "doctype": "Gym Member",
#                 "full_name": full_name,
#                 "email": doc.email,
#                 "phone_numer": doc.phone,
#                 "gender":doc.gender,
#                 "date_of_birth":doc.birth_date,

#             })
#             gym_member.insert(ignore_permissions=True)
#             frappe.db.commit()


def create_gym_member(doc, method):
    if any(role.role == "Gym Member" for role in doc.roles):
        # Check if the Gym Member already exists
        if not frappe.db.exists("Gym Member", {"email": doc.email}):
            full_name = (
                doc.full_name
                if hasattr(doc, "full_name") and doc.full_name
                else f"{doc.first_name or ''} {doc.last_name or ''}".strip()
            )

            if not full_name:
                frappe.throw("Cannot create Gym Member without a full name.")

            gym_member = frappe.get_doc({
                "doctype": "Gym Member",
                "full_name": full_name,
                "email": doc.email,
                "phone_number": doc.phone,
                "gender": doc.gender,
                "date_of_birth": doc.birth_date,
                "user": doc.name
            })

            gym_member.insert(ignore_permissions=True)
            frappe.db.commit()

def create_gym_trainer(doc, method):
    if hasattr(doc, "roles") and any(role.role == "Gym Trainer" for role in doc.roles):
        if not frappe.db.exists("Gym Trainer", {"email": doc.email}):
            full_name = (
                doc.full_name
                if hasattr(doc, "full_name") and doc.full_name
                else f"{doc.first_name or ''} {doc.last_name or ''}".strip()
            )

            gym_trainer = frappe.get_doc({
                "doctype": "Gym Trainer",
                "full_name": full_name,
                "email": doc.email,
                "phone_number": doc.phone,
                "gender": doc.gender,
                "date_of_birth": doc.birth_date,
                "user": doc.name,
            })
            gym_trainer.insert(ignore_permissions=True)
            frappe.db.commit()

            frappe.msgprint(
                f"""Trainer profile created.<br>
                <a href="/app/gym-trainer/{gym_trainer.name}" style="color:#007bff;">Click here to update</a>.""",
                title="Trainer Created",
                indicator="green"
            )


# def custom_login_redirect(login_manager):
#     user = login_manager.user
#     roles = frappe.get_roles(user)

#     if "Gym Member" in roles:
#         frappe.local.response["type"] = "redirect"
#         frappe.local.response["location"] = "/member_home"
