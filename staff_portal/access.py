from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


ACCESS_FIELDS = [
    ("requested_finance", "مالی", "finance-operator", "کارشناس مالی"),
    ("requested_hr", "منابع انسانی", "hr-operator", "منابع انسانی"),
    ("requested_attendance", "حضور و غیاب", "attendance-operator", "حضور و غیاب"),
    ("requested_payroll", "حقوق و دستمزد", "payroll-operator", "حقوق و دستمزد"),
    ("requested_ticketing", "تیکتینگ", "ticket-operator", "تیکتینگ"),
    ("requested_datacenter", "دیتاسنتر", "datacenter-operator", "کارشناس دیتاسنتر"),
    ("requested_user_manager", "مدیریت کاربران", "user-manager", "مدیریت کاربران"),
]


ACCESS_PERMISSIONS = {
    "requested_finance": {
        ("accounting", "view_account"),
        ("accounting", "view_voucher"),
        ("accounting", "change_voucher"),
        ("core", "view_payment"),
        ("core", "change_payment"),
        ("core", "view_party"),
    },
    "requested_hr": {
        ("hr", "view_employeeprofile"),
        ("hr", "change_employeeprofile"),
        ("hr", "view_staffregistrationrequest"),
    },
    "requested_attendance": {
        ("hr", "view_attendance"),
        ("hr", "add_attendance"),
        ("hr", "change_attendance"),
        ("hr", "view_shift"),
        ("hr", "view_shiftassignment"),
        ("hr", "add_shiftassignment"),
        ("hr", "change_shiftassignment"),
    },
    "requested_payroll": {
        ("hr", "view_payroll"),
        ("hr", "add_payroll"),
        ("hr", "change_payroll"),
    },
    "requested_ticketing": {
        ("ticketing", "view_ticket"),
        ("ticketing", "add_ticket"),
        ("ticketing", "change_ticket"),
        ("ticketing", "view_ticketreply"),
        ("ticketing", "add_ticketreply"),
        ("ticketing", "change_ticketreply"),
    },
    "requested_datacenter": {
        ("datacenter", "view_serviceplan"),
        ("datacenter", "view_subscription"),
        ("datacenter", "change_subscription"),
        ("datacenter", "view_ipblock"),
        ("datacenter", "view_iplease"),
        ("datacenter", "view_pingtarget"),
        ("datacenter", "add_pingtarget"),
        ("datacenter", "change_pingtarget"),
        ("datacenter", "view_pingcheck"),
    },
    "requested_user_manager": {
        ("core", "view_user"),
        ("core", "change_user"),
        ("core", "view_role"),
        ("core", "change_role"),
        ("hr", "view_staffregistrationrequest"),
        ("hr", "change_staffregistrationrequest"),
    },
}


MODULE_POLICIES = {
    "finance": {
        "roles": {"finance-operator"},
        "permissions": {"accounting.view_account", "accounting.view_voucher", "core.view_payment"},
    },
    "hr": {
        "roles": {"hr-operator", "attendance-operator", "payroll-operator"},
        "permissions": {"hr.view_employeeprofile", "hr.view_attendance", "hr.view_payroll"},
    },
    "attendance": {
        "roles": {"attendance-operator", "hr-operator"},
        "permissions": {"hr.view_attendance", "hr.view_shiftassignment"},
    },
    "payroll": {
        "roles": {"payroll-operator", "hr-operator"},
        "permissions": {"hr.view_payroll"},
    },
    "ticketing": {
        "roles": {"ticket-operator"},
        "permissions": {"ticketing.view_ticket", "ticketing.change_ticket"},
    },
    "datacenter": {
        "roles": {"datacenter-operator"},
        "permissions": {"datacenter.view_pingtarget", "datacenter.view_subscription"},
    },
    "management": {
        "roles": {"user-manager"},
        "permissions": {"core.view_user", "hr.view_staffregistrationrequest"},
    },
}


def is_staff_portal_user(user):
    return bool(user and user.is_authenticated and user.is_active and user.is_staff)


def user_role_slugs(user):
    if not is_staff_portal_user(user):
        return set()
    return set(user.roles.values_list("slug", flat=True))


def user_can_access_module(user, module):
    if not is_staff_portal_user(user):
        return False
    if user.is_superuser:
        return True

    policy = MODULE_POLICIES.get(module)
    if not policy:
        return False

    roles = policy.get("roles", set())
    if roles and user_role_slugs(user).intersection(roles):
        return True

    return any(user.has_perm(permission) for permission in policy.get("permissions", set()))


def user_can_access_any_module(user, modules):
    return any(user_can_access_module(user, module) for module in modules)


def staff_module_required(*modules, login_url="/portal/login/"):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            user = request.user
            if not user or not user.is_authenticated:
                return redirect_to_login(request.get_full_path(), login_url)
            if not is_staff_portal_user(user):
                raise PermissionDenied
            if modules and not user_can_access_any_module(user, modules):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
