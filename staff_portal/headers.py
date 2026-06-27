from django.conf import settings


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault("X-Content-Type-Options", "nosniff")
        response.setdefault("Referrer-Policy", getattr(settings, "SECURE_REFERRER_POLICY", "strict-origin-when-cross-origin"))
        response.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=(), payment=()",
        )
        csp = getattr(settings, "CONTENT_SECURITY_POLICY_REPORT_ONLY", "")
        if csp:
            response.setdefault("Content-Security-Policy-Report-Only", csp)
        return response
