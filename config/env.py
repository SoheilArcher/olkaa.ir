from django.core.exceptions import ImproperlyConfigured


INSECURE_SECRET_KEYS = {
    "",
    "dev-insecure-change-me",
    "django-insecure",
}


def env_bool(environ, key, default=False):
    return environ.get(key, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def env_int(environ, key, default=0):
    raw_value = environ.get(key, str(default)).strip()
    try:
        return int(raw_value)
    except ValueError as exc:
        raise ImproperlyConfigured(f"{key} must be an integer.") from exc


def env_list(environ, key, default=""):
    return [item.strip() for item in environ.get(key, default).split(",") if item.strip()]


def is_production(environ, debug):
    return environ.get("DJANGO_ENV", "").strip().lower() == "production" or not debug


def validate_production_environment(environ, *, debug, secret_key, allowed_hosts):
    if not is_production(environ, debug):
        return

    missing = []
    if environ.get("DJANGO_ENV", "").strip().lower() == "production" and debug:
        missing.append("DEBUG=False")
    if not secret_key or secret_key in INSECURE_SECRET_KEYS or secret_key.startswith("dev-"):
        missing.append("SECRET_KEY")
    if not allowed_hosts or "*" in allowed_hosts:
        missing.append("ALLOWED_HOSTS")

    if missing:
        joined = ", ".join(missing)
        raise ImproperlyConfigured(
            f"Production environment is missing secure configuration for: {joined}."
        )
