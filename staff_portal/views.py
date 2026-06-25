from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from core.models import Role
from hr.models import Attendance, EmployeeProfile, Payroll, StaffRegistrationRequest

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
            "title": "واحد مالی",
            "caption": "کدینگ، اسناد، پرداخت‌ها و گزارش‌های مالی",
            "href": "/admin/accounting/",
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

    stats = [
        {"label": "در انتظار تایید", "value": pending_requests.count(), "caption": "بعد از تایید ایمیل"},
        {"label": "کارمندان فعال", "value": EmployeeProfile.objects.filter(status=EmployeeProfile.ACTIVE).count(), "caption": "پرونده پرسنلی"},
        {"label": "فیش‌های پرداخت‌نشده", "value": Payroll.objects.exclude(status=Payroll.PAID).count(), "caption": "حقوق و دستمزد"},
        {"label": "حضور امروز", "value": Attendance.objects.filter(date=timezone.localdate()).count(), "caption": "ثبت‌شده امروز"},
    ]
    return render(
        request,
        "staff_portal/manager.html",
        {
            "access_fields": ACCESS_FIELDS,
            "attendance_today": attendance_today,
            "employees": employees,
            "payrolls": payrolls,
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
