from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Permission
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from core.models import Role
from accounting.models import Expense, Invoice
from datacenter.models import PingCheck, PingTarget
from hr.models import Attendance, EmployeeProfile, Payroll, StaffRegistrationRequest
from ticketing.models import Ticket, TicketReply

from .forms import RegistrationCodeForm, StaffRegistrationForm


signer = TimestampSigner(salt="staff-registration")


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


def _is_staff_manager(user):
    return user.is_authenticated and user.is_staff


def _role(name, slug):
    role, _ = Role.objects.get_or_create(slug=slug, defaults={"name": name})
    return role


def _sync_registration_accesses(registration, request):
    for field, _label, _slug, _role_name in ACCESS_FIELDS:
        setattr(registration, field, request.POST.get(field) == "on")


def _approve_registration(registration, approver):
    registration.user.is_active = True
    registration.user.is_staff = True
    registration.user.save(update_fields=("is_active", "is_staff"))

    for field, _label, slug, role_name in ACCESS_FIELDS:
        if getattr(registration, field):
            registration.user.roles.add(_role(role_name, slug))
            for app_label, codename in ACCESS_PERMISSIONS.get(field, set()):
                permission = Permission.objects.filter(
                    content_type__app_label=app_label,
                    codename=codename,
                ).first()
                if permission:
                    registration.user.user_permissions.add(permission)

    EmployeeProfile.objects.get_or_create(
        user=registration.user,
        defaults={
            "personnel_code": f"EMP-{registration.user_id:05d}",
            "department": registration.requested_department,
            "job_title": registration.requested_job_title,
        },
    )
    registration.status = StaffRegistrationRequest.APPROVED
    registration.approved_at = timezone.now()
    registration.approved_by = approver
    registration.save()


@login_required
def dashboard(request):
    modules = [
        {
            "title": "اتاق کنترل زنده",
            "caption": "مانیتورینگ، تیکت‌ها، حضور امروز و رخدادهای جاری",
            "href": "/portal/live/",
            "status": "زنده",
        },
        {
            "title": "واحد مالی",
            "caption": "فاکتورها، هزینه‌ها، پرداخت‌ها و گزارش سریع",
            "href": "/portal/finance/",
            "status": "فعال",
        },
        {
            "title": "منابع انسانی",
            "caption": "پرونده پرسنلی، حضور و غیاب، مرخصی و حقوق",
            "href": "/admin/hr/",
            "status": "مرحله اول",
        },
        {
            "title": "تیکتینگ",
            "caption": "ارسال درخواست، ارجاع، اولویت‌بندی و پیگیری",
            "href": "/admin/ticketing/",
            "status": "مرحله اول",
        },
        {
            "title": "دیتاسنتر",
            "caption": "پلن‌ها، اشتراک‌ها، بلوک‌های IP و اجاره IP",
            "href": "/admin/datacenter/",
            "status": "مرحله اول",
        },
        {
            "title": "مدیریت کاربران",
            "caption": "تایید کارمندان، نقش‌ها و دسترسی‌های داخلی",
            "href": "/portal/manager/",
            "status": "فعال",
        },
        {
            "title": "ثبت‌نام کارمند",
            "caption": "فرم عضویت، تایید ایمیل و فعال‌سازی توسط مدیر",
            "href": "/portal/register/",
            "status": "عمومی",
        },
    ]
    return render(request, "staff_portal/dashboard.html", {"modules": modules})


@user_passes_test(_is_staff_manager, login_url="/admin/login/")
def finance(request):
    invoices = Invoice.objects.select_related("party").order_by("-issue_date", "-created_at")
    expenses = Expense.objects.select_related("party", "bank_account").order_by("-date", "-created_at")
    open_invoices = invoices.exclude(status__in=[Invoice.PAID, Invoice.CANCELED])
    paid_invoices = invoices.filter(status=Invoice.PAID)
    unpaid_expenses = expenses.exclude(status=Expense.PAID)
    paid_expenses = expenses.filter(status=Expense.PAID)

    paid_income = sum(invoice.total_rial for invoice in paid_invoices[:200])
    receivable = sum(invoice.total_rial for invoice in open_invoices[:200])
    paid_cost = sum(expense.amount_rial for expense in paid_expenses[:200])
    pending_cost = sum(expense.amount_rial for expense in unpaid_expenses[:200])

    stats = [
        {"label": "درآمد وصول‌شده", "value": f"{paid_income:,}", "caption": "ریال"},
        {"label": "مطالبات باز", "value": f"{receivable:,}", "caption": "ریال"},
        {"label": "هزینه پرداخت‌شده", "value": f"{paid_cost:,}", "caption": "ریال"},
        {"label": "هزینه در صف", "value": f"{pending_cost:,}", "caption": "ریال"},
    ]
    return render(
        request,
        "staff_portal/finance.html",
        {
            "expenses": expenses[:10],
            "invoices": invoices[:10],
            "open_invoices": open_invoices[:8],
            "unpaid_expenses": unpaid_expenses[:8],
            "stats": stats,
        },
    )


@user_passes_test(_is_staff_manager, login_url="/admin/login/")
def live(request):
    now = timezone.localtime()
    today = timezone.localdate()
    open_tickets = Ticket.objects.exclude(status=Ticket.CLOSED).select_related("requester", "assigned_to").order_by(
        "-priority",
        "-created_at",
    )[:10]
    urgent_tickets = Ticket.objects.filter(priority__in=[Ticket.HIGH, Ticket.URGENT]).exclude(status=Ticket.CLOSED)
    monitoring_targets = PingTarget.objects.order_by("last_status", "name")
    down_targets = monitoring_targets.filter(last_status=PingTarget.DOWN)
    attendance_today = Attendance.objects.filter(date=today).select_related("employee", "employee__user").order_by(
        "employee__personnel_code"
    )
    recent_registrations = StaffRegistrationRequest.objects.select_related("user").order_by("-created_at")[:6]
    payroll_queue = Payroll.objects.exclude(status=Payroll.PAID).select_related("employee", "employee__user").order_by(
        "-period",
        "-created_at",
    )[:6]

    recent_events = []
    for ticket in Ticket.objects.select_related("requester", "assigned_to").order_by("-created_at")[:8]:
        recent_events.append(
            {
                "time": ticket.created_at,
                "type": "تیکت",
                "title": ticket.title,
                "detail": f"{ticket.get_status_display()} / {ticket.get_priority_display()}",
                "href": f"/admin/ticketing/ticket/{ticket.pk}/change/",
            }
        )
    for reply in TicketReply.objects.select_related("ticket", "author").order_by("-created_at")[:8]:
        recent_events.append(
            {
                "time": reply.created_at,
                "type": "پاسخ",
                "title": reply.ticket.title,
                "detail": reply.author.get_full_name() or reply.author.email or reply.author.username,
                "href": f"/admin/ticketing/ticket/{reply.ticket_id}/change/",
            }
        )
    for check in PingCheck.objects.select_related("target").filter(status=PingTarget.DOWN).order_by("-created_at")[:8]:
        recent_events.append(
            {
                "time": check.created_at,
                "type": "مانیتورینگ",
                "title": check.target.name,
                "detail": "پینگ ناموفق",
                "href": f"/admin/datacenter/pingtarget/{check.target_id}/change/",
            }
        )
    for registration in recent_registrations:
        recent_events.append(
            {
                "time": registration.created_at,
                "type": "ثبت‌نام",
                "title": registration.user.get_full_name() or registration.user.email,
                "detail": registration.get_status_display(),
                "href": f"/admin/hr/staffregistrationrequest/{registration.pk}/change/",
            }
        )
    recent_events = sorted(recent_events, key=lambda item: item["time"], reverse=True)[:18]

    stats = [
        {"label": "سرورهای قطع", "value": down_targets.count(), "caption": "نیازمند بررسی سریع"},
        {"label": "تیکت‌های باز", "value": Ticket.objects.exclude(status=Ticket.CLOSED).count(), "caption": "در جریان"},
        {"label": "تیکت‌های فوری", "value": urgent_tickets.count(), "caption": "اولویت بالا"},
        {"label": "حضور امروز", "value": attendance_today.count(), "caption": "رکورد ثبت شده"},
        {
            "label": "در انتظار تایید",
            "value": StaffRegistrationRequest.objects.filter(status=StaffRegistrationRequest.PENDING_APPROVAL).count(),
            "caption": "ثبت‌نام کارمند",
        },
        {"label": "پرداخت‌نشده", "value": Payroll.objects.exclude(status=Payroll.PAID).count(), "caption": "حقوق و دستمزد"},
    ]
    return render(
        request,
        "staff_portal/live.html",
        {
            "attendance_today": attendance_today[:10],
            "monitoring_targets": monitoring_targets[:16],
            "down_targets": down_targets,
            "now": now,
            "open_tickets": open_tickets,
            "payroll_queue": payroll_queue,
            "recent_events": recent_events,
            "recent_registrations": recent_registrations,
            "stats": stats,
        },
    )


@user_passes_test(_is_staff_manager, login_url="/admin/login/")
def manager(request):
    if request.method == "POST":
        registration = get_object_or_404(
            StaffRegistrationRequest.objects.select_related("user"),
            pk=request.POST.get("registration_id"),
        )
        action = request.POST.get("action")
        if action == "approve":
            _sync_registration_accesses(registration, request)
            _approve_registration(registration, request.user)
            messages.success(request, "کارمند تایید شد و دسترسی‌ها فعال شدند.")
        elif action == "reject":
            registration.status = StaffRegistrationRequest.REJECTED
            registration.manager_note = request.POST.get("manager_note", "")
            registration.user.is_active = False
            registration.user.save(update_fields=("is_active",))
            registration.save(update_fields=("status", "manager_note", "updated_at"))
            messages.warning(request, "درخواست ثبت‌نام رد شد.")
        return redirect("staff_portal:manager")

    pending_requests = (
        StaffRegistrationRequest.objects.select_related("user")
        .filter(status=StaffRegistrationRequest.PENDING_APPROVAL)
        .order_by("created_at")
    )
    pending_cards = []
    for registration in pending_requests:
        pending_cards.append(
            {
                "registration": registration,
                "accesses": [
                    {
                        "field": field,
                        "label": label,
                        "checked": getattr(registration, field),
                    }
                    for field, label, _slug, _role_name in ACCESS_FIELDS
                ],
            }
        )
    recent_requests = StaffRegistrationRequest.objects.select_related("user").order_by("-created_at")[:8]
    employees = EmployeeProfile.objects.select_related("user").order_by("department", "personnel_code")[:12]
    payrolls = Payroll.objects.select_related("employee", "employee__user").order_by("-period", "-created_at")[:8]
    attendance_today = Attendance.objects.filter(date=timezone.localdate()).select_related("employee", "employee__user")[:8]
    monitoring_targets = PingTarget.objects.order_by("last_status", "name")[:12]

    stats = [
        {"label": "در انتظار تایید", "value": pending_requests.count(), "caption": "بعد از تایید ایمیل"},
        {"label": "کارمندان فعال", "value": EmployeeProfile.objects.filter(status=EmployeeProfile.ACTIVE).count(), "caption": "پرونده پرسنلی"},
        {"label": "فیش‌های پرداخت‌نشده", "value": Payroll.objects.exclude(status=Payroll.PAID).count(), "caption": "حقوق و دستمزد"},
        {"label": "مانیتورینگ قطع", "value": PingTarget.objects.filter(last_status=PingTarget.DOWN).count(), "caption": "پینگ ناموفق"},
    ]
    return render(
        request,
        "staff_portal/manager.html",
        {
            "access_fields": ACCESS_FIELDS,
            "attendance_today": attendance_today,
            "employees": employees,
            "payrolls": payrolls,
            "monitoring_targets": monitoring_targets,
            "pending_cards": pending_cards,
            "pending_requests": pending_requests,
            "recent_requests": recent_requests,
            "stats": stats,
        },
    )


def register(request):
    if not request.session.get("staff_registration_unlocked"):
        if request.method == "POST":
            code_form = RegistrationCodeForm(request.POST)
            if code_form.is_valid():
                request.session["staff_registration_unlocked"] = True
                return redirect("staff_portal:register")
        else:
            code_form = RegistrationCodeForm()
        return render(request, "staff_portal/register_gate.html", {"form": code_form})

    if request.method == "POST":
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save()
            token = signer.sign(registration.pk)
            verify_url = request.build_absolute_uri(
                reverse("staff_portal:verify_email", kwargs={"token": token})
            )
            context = {
                "registration": registration,
                "verify_url": verify_url,
                "site": get_current_site(request),
            }
            email_sent = True
            try:
                send_mail(
                    "تایید ثبت‌نام در پورتال فاوا ایمن الکا",
                    render_to_string("staff_portal/email_verification.txt", context),
                    None,
                    [registration.user.email],
                    fail_silently=False,
                    html_message=render_to_string("staff_portal/email_verification.html", context),
                )
            except (OSError, UnicodeError, BadHeaderError):
                email_sent = False
            return render(
                request,
                "staff_portal/register_done.html",
                {"registration": registration, "verify_url": verify_url, "email_sent": email_sent},
            )
    else:
        form = StaffRegistrationForm()
    return render(request, "staff_portal/register.html", {"form": form})


def verify_email(request, token):
    try:
        registration_id = signer.unsign(token, max_age=60 * 60 * 24 * 2)
    except SignatureExpired:
        return render(request, "staff_portal/verify_result.html", {"status": "expired"})
    except BadSignature:
        return render(request, "staff_portal/verify_result.html", {"status": "invalid"})

    registration = get_object_or_404(StaffRegistrationRequest, pk=registration_id)
    if registration.status == StaffRegistrationRequest.PENDING_EMAIL:
        registration.status = StaffRegistrationRequest.PENDING_APPROVAL
        registration.email_verified_at = timezone.now()
        registration.save(update_fields=("status", "email_verified_at", "updated_at"))
    return render(
        request,
        "staff_portal/verify_result.html",
        {"status": "ok", "registration": registration},
    )
