from django.db import models

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
