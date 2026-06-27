from django.conf import settings
from django.core.cache import cache


class ThrottleBlocked(Exception):
    pass


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _clean_identifier(identifier):
    return (identifier or "anonymous").strip().lower()[:120]


def throttle_key(scope, request, identifier=""):
    return f"staff-throttle:{scope}:{_client_ip(request)}:{_clean_identifier(identifier)}"


def throttle_limit(scope):
    limits = getattr(settings, "STAFF_PORTAL_THROTTLE_LIMITS", {})
    return limits.get(scope, limits.get("default", (10, 300)))


def check_throttle(scope, request, identifier=""):
    limit, window = throttle_limit(scope)
    key = throttle_key(scope, request, identifier)
    current = cache.get(key, 0)
    if current >= limit:
        raise ThrottleBlocked("درخواست‌های زیادی ثبت شده است. چند دقیقه بعد دوباره تلاش کنید.")
    return key


def register_attempt(scope, request, identifier=""):
    limit, window = throttle_limit(scope)
    key = throttle_key(scope, request, identifier)
    current = cache.get(key, 0)
    cache.set(key, current + 1, window)
    if current + 1 > limit:
        raise ThrottleBlocked("درخواست‌های زیادی ثبت شده است. چند دقیقه بعد دوباره تلاش کنید.")


def reset_attempts(scope, request, identifier=""):
    cache.delete(throttle_key(scope, request, identifier))
