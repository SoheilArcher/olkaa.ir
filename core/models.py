"""
مدل‌های هسته‌ی مشترک.

نکته‌ی طراحی: مدل مرکزی Party (طرف‌حساب) است که می‌تواند «شخص» یا «شرکت»
باشد و در همه‌ی ماژول‌ها (CRM، حسابداری، دیتاسنتر، تیکتینگ) استفاده می‌شود.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_national_id


class TimeStamped(models.Model):
    """مدل پایه با زمان ایجاد و ویرایش. تاریخ‌ها میلادی/UTC ذخیره می‌شوند."""

    created_at = models.DateTimeField("ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("ویرایش", auto_now=True)

    class Meta:
        abstract = True


class Role(TimeStamped):
    """نقش کاربری برای کنترل سطح‌دسترسی (RBAC)."""

    name = models.CharField("نام نقش", max_length=80)
    slug = models.SlugField("شناسه", max_length=80, unique=True)

    class Meta:
        verbose_name = "نقش"
        verbose_name_plural = "نقش‌ها"

    def __str__(self):
        return self.name


class Party(TimeStamped):
    """طرف‌حساب: مشتری/شخص/شرکت — هسته‌ی مشترک تمام ماژول‌ها."""

    PERSON = "person"
    COMPANY = "company"
    TYPE_CHOICES = [(PERSON, "شخص"), (COMPANY, "شرکت")]

    party_type = models.CharField("نوع", max_length=10, choices=TYPE_CHOICES, default=PERSON)
    name = models.CharField("نام", max_length=200)
    national_id = models.CharField(
        "کد ملی", max_length=10, blank=True, validators=[validate_national_id]
    )
    economic_code = models.CharField("کد اقتصادی", max_length=20, blank=True)
    mobile = models.CharField("موبایل", max_length=15, blank=True)
    email = models.EmailField("ایمیل", blank=True)
    is_customer = models.BooleanField("مشتری است", default=True)

    class Meta:
        verbose_name = "طرف‌حساب"
        verbose_name_plural = "طرف‌حساب‌ها"

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    کاربر سیستم. یک مدل واحد برای کارمند و مشتری؛ تفکیک با نقش‌ها.
    کاربرانِ مشتری به یک Party وصل می‌شوند.
    """

    party = models.ForeignKey(
        Party,
        verbose_name="طرف‌حساب",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    roles = models.ManyToManyField(Role, verbose_name="نقش‌ها", blank=True, related_name="users")

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


class Payment(TimeStamped):
    """رکورد پرداخت آنلاین (هسته‌ی مشترک؛ همه‌ی ماژول‌ها از آن استفاده می‌کنند)."""

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    STATUS_CHOICES = [
        (PENDING, "در انتظار"),
        (SUCCESS, "موفق"),
        (FAILED, "ناموفق"),
    ]

    party = models.ForeignKey(
        Party, verbose_name="پرداخت‌کننده", on_delete=models.PROTECT, related_name="payments"
    )
    amount_rial = models.BigIntegerField("مبلغ (ریال)")
    status = models.CharField("وضعیت", max_length=10, choices=STATUS_CHOICES, default=PENDING)
    gateway = models.CharField("درگاه", max_length=30, default="zarinpal")
    authority = models.CharField("کد مرجع درگاه", max_length=64, blank=True)
    ref_id = models.CharField("شناسه پیگیری", max_length=64, blank=True)

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"

    def __str__(self):
        return f"{self.party} — {self.amount_rial} ریال ({self.get_status_display()})"

    @property
    def amount_toman(self):
        return self.amount_rial // 10
