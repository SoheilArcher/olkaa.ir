from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from hr.models import StaffRegistrationRequest

from .forms import StaffRegistrationForm


signer = TimestampSigner(salt="staff-registration")


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
            "caption": "کاربران، نقش‌ها، طرف‌حساب‌ها و دسترسی‌ها",
            "href": "/admin/core/",
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


def register(request):
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
