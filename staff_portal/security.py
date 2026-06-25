from datetime import timedelta
import random

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import constant_time_compare, salted_hmac


OTP_VERIFIED_USER_ID = "email_otp_verified_user_id"
OTP_USER_ID = "email_otp_user_id"
OTP_CODE_HASH = "email_otp_code_hash"
OTP_SENT_AT = "email_otp_sent_at"
OTP_EXPIRES_AT = "email_otp_expires_at"
OTP_LAST_ERROR = "email_otp_last_error"


def _timestamp(value):
    return int(value.timestamp())


def _hash_code(user, code):
    return salted_hmac(
        "staff_portal.email_otp",
        f"{user.pk}:{code}",
    ).hexdigest()


def is_otp_verified(request):
    if not getattr(settings, "EMAIL_OTP_ENABLED", True):
        return True
    user = getattr(request, "user", None)
    return bool(
        user
        and user.is_authenticated
        and request.session.get(OTP_VERIFIED_USER_ID) == user.pk
    )


def clear_otp_challenge(request):
    for key in (
        OTP_USER_ID,
        OTP_CODE_HASH,
        OTP_SENT_AT,
        OTP_EXPIRES_AT,
        OTP_LAST_ERROR,
    ):
        request.session.pop(key, None)


def _active_challenge_exists(request):
    user = request.user
    expires_at = request.session.get(OTP_EXPIRES_AT)
    return bool(
        request.session.get(OTP_USER_ID) == user.pk
        and request.session.get(OTP_CODE_HASH)
        and expires_at
        and expires_at > _timestamp(timezone.now())
    )


def ensure_otp_challenge(request, force=False):
    user = request.user
    if is_otp_verified(request):
        return True
    if not force and _active_challenge_exists(request):
        return True

    clear_otp_challenge(request)
    code = f"{random.SystemRandom().randint(0, 999999):06d}"
    now = timezone.now()
    expires_at = now + timedelta(minutes=getattr(settings, "EMAIL_OTP_EXPIRE_MINUTES", 10))

    request.session[OTP_USER_ID] = user.pk
    request.session[OTP_CODE_HASH] = _hash_code(user, code)
    request.session[OTP_SENT_AT] = _timestamp(now)
    request.session[OTP_EXPIRES_AT] = _timestamp(expires_at)

    recipient = (user.email or "").strip()
    if not recipient:
        request.session[OTP_LAST_ERROR] = "برای این کاربر ایمیل ثبت نشده است."
        return False

    context = {
        "code": code,
        "expires_at": expires_at,
        "user": user,
    }
    try:
        send_mail(
            "کد ورود امن فاوا ایمن الکا",
            render_to_string("staff_portal/login_otp_email.txt", context),
            None,
            [recipient],
            fail_silently=False,
        )
    except Exception:
        request.session[OTP_LAST_ERROR] = "ارسال ایمیل کد ورود کامل نشد. تنظیمات ایمیل یا صندوق مقصد را بررسی کنید."
        return False

    request.session.pop(OTP_LAST_ERROR, None)
    return True


def verify_otp_code(request, code):
    if not _active_challenge_exists(request):
        return False, "کد ورود منقضی شده است. دوباره کد بگیرید."

    expected = request.session.get(OTP_CODE_HASH, "")
    if not constant_time_compare(expected, _hash_code(request.user, code.strip())):
        return False, "کد وارد شده درست نیست."

    request.session[OTP_VERIFIED_USER_ID] = request.user.pk
    clear_otp_challenge(request)
    return True, ""
