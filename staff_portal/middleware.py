from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from .security import ensure_otp_challenge, is_otp_verified


class EmailOtpMiddleware:
    protected_prefixes = ("/admin/", "/portal/")
    exempt_prefixes = (
        "/admin/login/",
        "/admin/logout/",
        "/portal/otp/",
        "/portal/register/",
        "/portal/verify/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._must_verify(request):
            ensure_otp_challenge(request)
            query = urlencode({"next": request.get_full_path()})
            return redirect(f"{reverse('staff_portal:email_otp')}?{query}")
        return self.get_response(request)

    def _must_verify(self, request):
        if not getattr(settings, "EMAIL_OTP_ENABLED", True):
            return False
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        path = request.path_info or "/"
        if path.startswith(self.exempt_prefixes):
            return False
        if not path.startswith(self.protected_prefixes):
            return False
        return not is_otp_verified(request)
