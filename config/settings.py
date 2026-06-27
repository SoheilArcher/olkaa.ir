"""
تنظیمات پروژه‌ی فاوا ایمن اُلکا.

به‌صورت پیش‌فرض با SQLite اجرا می‌شود تا بدون نصب چیزی بالا بیاید.
برای PostgreSQL کافی است متغیرهای POSTGRES_* را در فایل .env پر کنید.
"""
from pathlib import Path
import os

from .env import env_bool, env_int, env_list, validate_production_environment

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-change-me")
DEBUG = env_bool(os.environ, "DEBUG", True)
ALLOWED_HOSTS = env_list(os.environ, "ALLOWED_HOSTS", "*" if DEBUG else "")
CSRF_TRUSTED_ORIGINS = env_list(os.environ, "CSRF_TRUSTED_ORIGINS")
validate_production_environment(
    os.environ,
    debug=DEBUG,
    secret_key=SECRET_KEY,
    allowed_hosts=ALLOWED_HOSTS,
)

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps پروژه
    "core",
    "website",
    "accounting",
    "staff_portal",
    "hr",
    "ticketing",
    "datacenter",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "staff_portal.headers.SecurityHeadersMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "staff_portal.middleware.EmailOtpMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# پایگاه داده: پیش‌فرض SQLite، در صورت تعریف POSTGRES_DB از PostgreSQL استفاده می‌شود
if os.environ.get("POSTGRES_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["POSTGRES_DB"],
            "USER": os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_USER_MODEL = "core.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.environ.get("STATIC_ROOT", BASE_DIR / "staticfiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/admin/login/"

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "mail.cipikia.co")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool(os.environ, "EMAIL_USE_TLS", True)
EMAIL_USE_SSL = env_bool(os.environ, "EMAIL_USE_SSL", False)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "admin@olkaa.ir")
STAFF_REGISTRATION_CODE = os.environ.get("STAFF_REGISTRATION_CODE", "")
MONITORING_ALERT_EMAILS = os.environ.get("MONITORING_ALERT_EMAILS", DEFAULT_FROM_EMAIL)
EMAIL_OTP_ENABLED = env_bool(os.environ, "EMAIL_OTP_ENABLED", True)
EMAIL_OTP_EXPIRE_MINUTES = int(os.environ.get("EMAIL_OTP_EXPIRE_MINUTES", "10"))
STAFF_PORTAL_THROTTLE_LIMITS = {
    "default": (
        env_int(os.environ, "STAFF_THROTTLE_DEFAULT_LIMIT", 10),
        env_int(os.environ, "STAFF_THROTTLE_DEFAULT_WINDOW", 300),
    ),
    "login": (
        env_int(os.environ, "STAFF_LOGIN_THROTTLE_LIMIT", 5),
        env_int(os.environ, "STAFF_LOGIN_THROTTLE_WINDOW", 300),
    ),
    "otp": (
        env_int(os.environ, "STAFF_OTP_THROTTLE_LIMIT", 5),
        env_int(os.environ, "STAFF_OTP_THROTTLE_WINDOW", 300),
    ),
    "otp_resend": (
        env_int(os.environ, "STAFF_OTP_RESEND_THROTTLE_LIMIT", 3),
        env_int(os.environ, "STAFF_OTP_RESEND_THROTTLE_WINDOW", 300),
    ),
    "registration": (
        env_int(os.environ, "STAFF_REGISTRATION_THROTTLE_LIMIT", 5),
        env_int(os.environ, "STAFF_REGISTRATION_THROTTLE_WINDOW", 300),
    ),
}

SECURE_SSL_REDIRECT = env_bool(os.environ, "SECURE_SSL_REDIRECT", False)
SESSION_COOKIE_SECURE = env_bool(os.environ, "SESSION_COOKIE_SECURE", False)
CSRF_COOKIE_SECURE = env_bool(os.environ, "CSRF_COOKIE_SECURE", False)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = env_bool(os.environ, "CSRF_COOKIE_HTTPONLY", False)
SECURE_HSTS_SECONDS = env_int(os.environ, "SECURE_HSTS_SECONDS", 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(os.environ, "SECURE_HSTS_INCLUDE_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = env_bool(os.environ, "SECURE_HSTS_PRELOAD", False)
X_FRAME_OPTIONS = os.environ.get("X_FRAME_OPTIONS", "DENY")
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = os.environ.get("SECURE_REFERRER_POLICY", "strict-origin-when-cross-origin")
CONTENT_SECURITY_POLICY_REPORT_ONLY = os.environ.get(
    "CONTENT_SECURITY_POLICY_REPORT_ONLY",
    "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self' 'unsafe-inline'",
)

# ----- ظاهر پنل مدیریت (Unfold) -----
UNFOLD = {
    "SITE_TITLE": "سامانه فاوا ایمن اُلکا",
    "SITE_HEADER": "فاوا ایمن اُلکا",
    "SITE_SYMBOL": "apartment",
    "SHOW_HISTORY": True,
    "COLORS": {
        "primary": {
            "50": "250 244 230", "100": "243 232 208", "200": "233 213 168",
            "300": "222 187 120", "400": "205 165 95", "500": "195 154 77",
            "600": "154 121 60", "700": "120 94 47", "800": "90 70 35",
            "900": "60 47 24", "950": "33 26 13",
        },
    },
}
