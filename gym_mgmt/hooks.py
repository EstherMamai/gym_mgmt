app_name = "gym_mgmt"
app_title = "Gym Membership Management App"
app_publisher = "Esther Mamai"
app_description = "This app manages gym membership"
app_email = "mamaiesther07@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "gym_mgmt",
# 		"logo": "/assets/gym_mgmt/logo.png",
# 		"title": "Gym Membership Management App",
# 		"route": "/gym_mgmt",
# 		"has_permission": "gym_mgmt.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/gym_mgmt/css/gym_mgmt.css"
# app_include_js = "/assets/gym_mgmt/js/gym_mgmt.js"

# include js, css files in header of web template
# web_include_css = "/assets/gym_mgmt/css/gym_mgmt.css"
# web_include_js = "/assets/gym_mgmt/js/gym_mgmt.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "gym_mgmt/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "gym_mgmt/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#     "Gym Member": "/member_home",
#     "Gym Trainer": "/trainer_home"
# }
# app_name = "gym_mgmt"
# website_context = {
#     "js": ["/assets/gym_mgmt/js/login_redirect.js"]
# }

# Safter_login = "gym_mgmt.handle_login_redirect"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "gym_mgmt.utils.jinja_methods",
# 	"filters": "gym_mgmt.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "gym_mgmt.install.before_install"
# after_install = "gym_mgmt.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "gym_mgmt.uninstall.before_uninstall"
# after_uninstall = "gym_mgmt.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "gym_mgmt.utils.before_app_install"
# after_app_install = "gym_mgmt.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "gym_mgmt.utils.before_app_uninstall"
# after_app_uninstall = "gym_mgmt.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gym_mgmt.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
    "Gym Membership": {
        "before_save": "gym_mgmt.services.rest.update_membership_status"
    },
    "Gym Trainer Subscription": {
        "before_save": "gym_mgmt.services.rest.update_membership_status"
    },
    "User": {
        "after_insert": [
            "gym_mgmt.services.rest.create_gym_member",
            "gym_mgmt.services.rest.create_gym_trainer"
        ],
        "on_update": [
            "gym_mgmt.services.rest.create_gym_member",
            "gym_mgmt.services.rest.create_gym_trainer"
        ]
    }
    # "User": {
    #     "on_update": "gym_mgmt.services.rest.create_gym_member"
    # },
    # "User": {
    #     "after_insert": "gym_mgmt.services.rest.create_gym_member"
	# },
    # "User": {
    #     "on_update": "gym_mgmt.services.rest.create_gym_trainer"
    # },
    # "User":{
    #     "after_insert": "gym_mgmt.services.rest.create_gym_trainer"
	# }
    # "Gym Locker Booking": {
    #     "before_save": "gym_mgmt.services.rest.update_locker_booking_status"
    # }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"gym_mgmt.tasks.all"
	# ],
	"daily": [
		"gym_mgmt.service.rest.update_locker_booking_status",
        "gym_mgmt.service.rest.update_class_booking_status"
	]
	# "hourly": [
	# 	"gym_mgmt.tasks.hourly"
	# ],
	# "weekly": [
	# 	"gym_mgmt.tasks.weekly"
	# ],
	# "monthly": [
	# 	"gym_mgmt.tasks.monthly"
	# ],
}

# Testing
# -------

# before_tests = "gym_mgmt.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gym_mgmt.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "gym_mgmt.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["gym_mgmt.utils.before_request"]
# after_request = ["gym_mgmt.utils.after_request"]

# Job Events
# ----------
# before_job = ["gym_mgmt.utils.before_job"]
# after_job = ["gym_mgmt.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"gym_mgmt.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# home"  # Default page for other rolesdef get_context(context):
#     user = frappe.session.user
#     if user != "Guest":
#         roles = frappe.get_roles(user)
#         if "Gym Member" in roles:
#             context.home_page = "member-home"
#         elif "Gym Admin" in roles:
#             context.home_page = "gym-admin-dashboard"
#         elif "Gym Trainer" in roles:
#             context.home_page = "gym-trainer-dashboard"
#         else:
#             context.home_page = "
# import frappe
# from frappe.utils import get_url

# def boot_session(bootinfo):
#     if bootinfo.user.name != "Guest":
#         roles = frappe.get_roles()
#         if "Gym Member" in roles:
#             bootinfo.home_page = "member_home"
#         elif "Gym Admin" in roles:
#             bootinfo.home_page = "gym_admin_dashboard"
#         elif "Gym Trainer" in roles:
#             bootinfo.home_page = "gym_trainer_dashboard"
#         else:
#             bootinfo.home_page = "home"

controller_hooks = {
    "User": {
        "after_save": "gym_mgmt.services.rest.handle_post_save_redirect"
    }
}