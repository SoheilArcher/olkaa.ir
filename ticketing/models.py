from django.conf import settings
from django.db import models

from core.models import Party, TimeStamped


class Ticket(TimeStamped):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    PRIORITY_CHOICES = [
        (LOW, "کم"),
        (NORMAL, "عادی"),
        (HIGH, "بالا"),
        (URGENT, "فوری"),
    ]

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    CLOSED = "closed"
    STATUS_CHOICES = [
        (OPEN, "باز"),
        (IN_PROGRESS, "در حال بررسی"),
        (WAITING, "در انتظار پاسخ"),
        (CLOSED, "بسته"),
    ]

    title = models.CharField("عنوان", max_length=180)
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="درخواست‌دهنده",
        on_delete=models.PROTECT,
        related_name="created_tickets",
    )
    party = models.ForeignKey(
        Party, verbose_name="طرف‌حساب", on_delete=models.SET_NULL, null=True, blank=True
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="مسئول رسیدگی",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )
    department = models.CharField("واحد مرتبط", max_length=80, blank=True)
    priority = models.CharField("اولویت", max_length=10, choices=PRIORITY_CHOICES, default=NORMAL)
    status = models.CharField("وضعیت", max_length=15, choices=STATUS_CHOICES, default=OPEN)
    description = models.TextField("شرح درخواست")

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت‌ها"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class TicketReply(TimeStamped):
    ticket = models.ForeignKey(Ticket, verbose_name="تیکت", on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="نویسنده", on_delete=models.PROTECT)
    message = models.TextField("پیام")
    is_internal = models.BooleanField("یادداشت داخلی", default=False)

    class Meta:
        verbose_name = "پاسخ تیکت"
        verbose_name_plural = "پاسخ‌های تیکت"
        ordering = ("created_at",)

    def __str__(self):
        return f"پاسخ {self.author} برای {self.ticket}"
