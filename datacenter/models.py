from django.db import models
from django.utils import timezone

from core.models import Party, TimeStamped


class ServicePlan(TimeStamped):
    INTERNET = "internet"
    BANDWIDTH = "bandwidth"
    IP_LEASE = "ip_lease"
    COLOCATION = "colocation"
    TYPE_CHOICES = [
        (INTERNET, "اینترنت"),
        (BANDWIDTH, "پهنای باند"),
        (IP_LEASE, "اجاره IP"),
        (COLOCATION, "کولوکیشن"),
    ]

    title = models.CharField("عنوان پلن", max_length=120)
    service_type = models.CharField("نوع سرویس", max_length=20, choices=TYPE_CHOICES)
    monthly_price_rial = models.BigIntegerField("قیمت ماهانه (ریال)", default=0)
    bandwidth_mbps = models.PositiveIntegerField("پهنای باند (Mbps)", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "پلن سرویس"
        verbose_name_plural = "پلن‌های سرویس"
        ordering = ("service_type", "title")

    def __str__(self):
        return self.title


class Subscription(TimeStamped):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    STATUS_CHOICES = [
        (ACTIVE, "فعال"),
        (SUSPENDED, "تعلیق"),
        (EXPIRED, "منقضی"),
    ]

    party = models.ForeignKey(Party, verbose_name="مشتری", on_delete=models.PROTECT, related_name="subscriptions")
    plan = models.ForeignKey(ServicePlan, verbose_name="پلن", on_delete=models.PROTECT, related_name="subscriptions")
    start_date = models.DateField("شروع")
    end_date = models.DateField("پایان")
    status = models.CharField("وضعیت", max_length=12, choices=STATUS_CHOICES, default=ACTIVE)
    circuit_id = models.CharField("شناسه سرویس/لینک", max_length=80, blank=True)
    note = models.CharField("توضیح", max_length=255, blank=True)

    class Meta:
        verbose_name = "اشتراک دیتاسنتر"
        verbose_name_plural = "اشتراک‌های دیتاسنتر"
        ordering = ("-end_date",)

    def __str__(self):
        return f"{self.party} — {self.plan}"


class IPBlock(TimeStamped):
    cidr = models.CharField("بلوک IP/CIDR", max_length=50, unique=True)
    owner = models.CharField("مالک/منبع", max_length=120, blank=True)
    total_addresses = models.PositiveIntegerField("تعداد آدرس", default=0)
    is_available = models.BooleanField("قابل واگذاری", default=True)
    note = models.CharField("توضیح", max_length=255, blank=True)

    class Meta:
        verbose_name = "بلوک IP"
        verbose_name_plural = "بلوک‌های IP"
        ordering = ("cidr",)

    def __str__(self):
        return self.cidr


class IPLease(TimeStamped):
    ACTIVE = "active"
    RELEASED = "released"
    STATUS_CHOICES = [
        (ACTIVE, "فعال"),
        (RELEASED, "آزاد شده"),
    ]

    block = models.ForeignKey(IPBlock, verbose_name="بلوک", on_delete=models.PROTECT, related_name="leases")
    party = models.ForeignKey(Party, verbose_name="مشتری", on_delete=models.PROTECT, related_name="ip_leases")
    assigned_cidr = models.CharField("محدوده واگذار شده", max_length=50)
    start_date = models.DateField("شروع")
    end_date = models.DateField("پایان", null=True, blank=True)
    status = models.CharField("وضعیت", max_length=12, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        verbose_name = "اجاره IP"
        verbose_name_plural = "اجاره‌های IP"
        ordering = ("-start_date",)

    def __str__(self):
        return f"{self.assigned_cidr} — {self.party}"


class PingTarget(TimeStamped):
    UP = "up"
    DOWN = "down"
    UNKNOWN = "unknown"
    STATUS_CHOICES = [
        (UP, "آنلاین"),
        (DOWN, "قطع"),
        (UNKNOWN, "نامشخص"),
    ]
    WEBSITE = "website"
    SERVER = "server"
    MAIL = "mail"
    NETWORK = "network"
    OTHER = "other"
    TARGET_TYPE_CHOICES = [
        (WEBSITE, "سایت"),
        (SERVER, "سرور"),
        (MAIL, "ایمیل"),
        (NETWORK, "شبکه"),
        (OTHER, "سایر"),
    ]
    PRODUCTION = "production"
    STAGING = "staging"
    INTERNAL = "internal"
    ENVIRONMENT_CHOICES = [
        (PRODUCTION, "Production"),
        (STAGING, "Staging"),
        (INTERNAL, "Internal"),
    ]

    name = models.CharField("نام سرویس", max_length=140)
    host = models.CharField("آدرس/IP", max_length=255, unique=True)
    target_type = models.CharField("نوع", max_length=20, choices=TARGET_TYPE_CHOICES, default=SERVER)
    environment = models.CharField("محیط", max_length=20, choices=ENVIRONMENT_CHOICES, default=PRODUCTION)
    support_owner = models.CharField("مسئول/تیم پشتیبانی", max_length=120, blank=True)
    support_hint = models.CharField("راهنمای اقدام هنگام قطعی", max_length=255, blank=True)
    alert_emails = models.CharField(
        "ایمیل‌های هشدار",
        max_length=500,
        blank=True,
        help_text="چند ایمیل را با کاما جدا کنید.",
    )
    is_active = models.BooleanField("فعال", default=True)
    last_status = models.CharField("آخرین وضعیت", max_length=10, choices=STATUS_CHOICES, default=UNKNOWN)
    last_latency_ms = models.PositiveIntegerField("آخرین تاخیر (ms)", null=True, blank=True)
    last_checked_at = models.DateTimeField("آخرین بررسی", null=True, blank=True)
    last_alert_sent_at = models.DateTimeField("آخرین هشدار ایمیلی", null=True, blank=True)
    failure_count = models.PositiveIntegerField("تعداد خطای پیاپی", default=0)
    note = models.CharField("توضیح", max_length=255, blank=True)

    class Meta:
        verbose_name = "هدف مانیتورینگ"
        verbose_name_plural = "مانیتورینگ پینگ"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} — {self.host}"

    def record_check(self, is_up, latency_ms=None, output=""):
        previous_status = self.last_status
        status = self.UP if is_up else self.DOWN
        self.last_status = status
        self.last_latency_ms = latency_ms if is_up else None
        self.last_checked_at = timezone.now()
        self.failure_count = 0 if is_up else self.failure_count + 1
        self.save(
            update_fields=(
                "last_status",
                "last_latency_ms",
                "last_checked_at",
                "failure_count",
                "updated_at",
            )
        )
        return PingCheck.objects.create(
            target=self,
            status=status,
            latency_ms=self.last_latency_ms,
            output=output[:1000],
            status_changed=previous_status != status,
        )

    @property
    def alert_recipients(self):
        return [email.strip() for email in self.alert_emails.split(",") if email.strip()]


class PingCheck(TimeStamped):
    target = models.ForeignKey(PingTarget, verbose_name="هدف", on_delete=models.CASCADE, related_name="checks")
    status = models.CharField("وضعیت", max_length=10, choices=PingTarget.STATUS_CHOICES)
    latency_ms = models.PositiveIntegerField("تاخیر (ms)", null=True, blank=True)
    output = models.TextField("خروجی", blank=True)
    status_changed = models.BooleanField("تغییر وضعیت", default=False)
    alert_sent_at = models.DateTimeField("زمان ارسال هشدار", null=True, blank=True)

    class Meta:
        verbose_name = "نتیجه پینگ"
        verbose_name_plural = "نتایج پینگ"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.target} — {self.get_status_display()}"
