# apps/gym_mgmt/gym_mgmt/api/rest.py
import frappe
from frappe import _
from frappe.utils import nowdate, now_datetime

@frappe.whitelist()
def update_membership_status(doc, method):
    """
    Automatically sets the status of Gym Membership based on dates.
    """
    today = nowdate()
    if doc.status == "Cancelled":
        return
    if doc.end_date and today > doc.end_date:
        doc.status = "Expired"
    elif doc.start_date and doc.start_date <= today <= doc.end_date:
        doc.status = "Active"
    elif doc.start_date and today < doc.start_date:
        doc.status = "Upcoming"

def update_locker_booking_status():
    today = nowdate()
    time_now = now_datetime().time()
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
    time_now = now_datetime().time()
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

def create_gym_member(doc, method):
    if any(role.role == "Gym Member" for role in doc.roles):
        if not frappe.db.exists("Gym Member", {"email": doc.email}):
            full_name = (
                getattr(doc, "full_name", None) or
                f"{doc.first_name or ''} {doc.last_name or ''}".strip()
            )
            if not full_name:
                frappe.log_error(f"Cannot create Gym Member without a full name for {doc.email}")
                return
            gym_member = frappe.get_doc({
                "doctype": "Gym Member",
                "full_name": full_name,
                "email": doc.email,
                "phone_number": getattr(doc, "mobile_no", None) or getattr(doc, "phone", None),
                "gender": getattr(doc, "gender", "Other"),
                "date_of_birth": getattr(doc, "birth_date", None),
                "user": doc.name
            })
            try:
                gym_member.insert(ignore_permissions=True)
                frappe.db.commit()
                frappe.log(f"Gym Member created for {doc.email}")
            except Exception as e:
                frappe.log_error(f"Error creating Gym Member for {doc.email}: {str(e)}")

# def create_gym_trainer(doc, method):
#     # if any(role.role == "Gym Trainer" for role in doc.roles):
#     if hasattr(doc, "roles") and any(role.role == "Gym Trainer" for role in doc.roles):
#         if not frappe.db.exists("Gym Trainer", {"email": doc.email}):
#             full_name = (
#                 getattr(doc, "full_name", None) or
#                 f"{doc.first_name or ''} {doc.last_name or ''}".strip()
#             )
#             if not full_name:
#                 frappe.log_error(f"Cannot create Gym Trainer without a full name for {doc.email}")
#                 return
#             gym_trainer = frappe.get_doc({
#                 "doctype": "Gym Trainer",
#                 "full_name": full_name,
#                 "email": doc.email,
#                 "phone_number": getattr(doc, "mobile_no", None) or getattr(doc, "phone", None),
#                 "gender": getattr(doc, "gender", "Other"),
#                 # "date_of_birth": getattr(doc, "birth_date", None),
#                 "user": doc.name
#             })
#             try:
#                 gym_trainer.insert(ignore_permissions=True)
#                 frappe.db.commit()
#                 frappe.log(f"Gym Trainer created for {doc.email}")
#                 # Store redirect info in session for post-save handling
#                 if "Gym Admin" in frappe.get_roles(frappe.session.user):
#                     frappe.local.redirect_location = f"/app/gym-trainer/{gym_trainer.name}"
#                 else:
#                     frappe.msgprint(
#                         f"""Trainer profile created.<br>
#                         <a href="/app/gym-trainer/{gym_trainer.name}" style="color:#007bff;">Click here to update</a>.""",
#                         title="Trainer Created",
#                         indicator="green"
#                     )
#             except Exception as e:
#                 frappe.log_error(f"Error creating Gym Trainer for {doc.email}: {str(e)}")
                
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

@frappe.whitelist()
def subscribe_to_trainer(trainer, start_date, end_date):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to subscribe"), frappe.PermissionError)
    if "Gym Member" not in frappe.get_roles():
        frappe.throw(_("You do not have permission to subscribe"), frappe.PermissionError)
    gym_member = frappe.get_all(
        "Gym Member",
        filters={"email": frappe.session.user},
        fields=["name"],
        limit=1
    )
    if not gym_member:
        frappe.throw(_("No Gym Member profile found"), frappe.DoesNotExistError)
    subscription = frappe.get_doc({
        "doctype": "Gym Trainer Subscription",
        "gym_member": gym_member[0].name,
        "trainer": trainer,
        "start_date": start_date,
        "end_date": end_date,
        "status": "Active"
    })
    subscription.insert(ignore_permissions=False)
    frappe.db.commit()
    return {"status": "success"}

@frappe.whitelist()
def get_trainer_members(trainer_email=None):
    if not trainer_email:
        frappe.throw(_("Trainer email is required"))
    trainer = frappe.get_all("Gym Trainer", filters={"email": trainer_email}, fields=["name"], limit=1)
    if not trainer:
        return []
    subscriptions = frappe.get_all(
        "Gym Trainer Subscription",
        filters={"trainer": trainer[0].name, "status": "Active"},
        fields=["gym_member"]
    )
    member_ids = [s.gym_member for s in subscriptions]
    members = frappe.get_all(
        "Gym Member",
        filters={"name": ["in", member_ids]},
        fields=["name", "full_name"]
    )
    return members

# Add to the end of apps/gym_mgmt/gym_mgmt/api/rest.py
def handle_post_save_redirect(doc, method):
    if hasattr(frappe.local, "redirect_location"):
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = frappe.local.redirect_location
        del frappe.local.redirect_location  # Clear to avoid reuse