from django.conf import settings
from django.db import models

from core.models import TimeStamped


class EmployeeProfile(TimeStamped):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    LEFT = "left"
    STATUS_CHOICES = [
        (ACTIVE, "فعال"),
        (SUSPENDED, "تعلیق"),
        (LEFT, "قطع همکاری"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="کاربر",
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )
    personnel_code = models.CharField("کد پرسنلی", max_length=30, unique=True)
    job_title = models.CharField("عنوان شغلی", max_length=120, blank=True)
    department = models.CharField("واحد", max_length=80, blank=True)
    hire_date = models.DateField("تاریخ شروع همکاری", null=True, blank=True)
    base_salary_rial = models.BigIntegerField("حقوق پایه (ریال)", default=0)
    status = models.CharField("وضعیت", max_length=12, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        verbose_name = "پرونده پرسنلی"
        verbose_name_plural = "پرونده‌های پرسنلی"
        ordering = ("personnel_code",)

    def __str__(self):
        return f"{self.personnel_code} — {self.user.get_full_name() or self.user.username}"


class Attendance(TimeStamped):
    PRESENT = "present"
    REMOTE = "remote"
    LEAVE = "leave"
    ABSENT = "absent"
    STATUS_CHOICES = [
        (PRESENT, "حاضر"),
        (REMOTE, "دورکاری"),
        (LEAVE, "مرخصی"),
        (ABSENT, "غیبت"),
    ]

    employee = models.ForeignKey(
        EmployeeProfile, verbose_name="کارمند", on_delete=models.CASCADE, related_name="attendances"
    )
    date = models.DateField("تاریخ")
    check_in = models.TimeField("ورود", null=True, blank=True)
    check_out = models.TimeField("خروج", null=True, blank=True)
    status = models.CharField("وضعیت", max_length=10, choices=STATUS_CHOICES, default=PRESENT)
    note = models.CharField("توضیح", max_length=255, blank=True)

    class Meta:
        verbose_name = "حضور و غیاب"
        verbose_name_plural = "حضور و غیاب"
        unique_together = ("employee", "date")
        ordering = ("-date", "employee")

    def __str__(self):
        return f"{self.employee} — {self.date}"


class Payroll(TimeStamped):
    DRAFT = "draft"
    APPROVED = "approved"
    PAID = "paid"
    STATUS_CHOICES = [
        (DRAFT, "پیش‌نویس"),
        (APPROVED, "تأیید شده"),
        (PAID, "پرداخت شده"),
    ]

    employee = models.ForeignKey(
        EmployeeProfile, verbose_name="کارمند", on_delete=models.PROTECT, related_name="payrolls"
    )
    period = models.CharField("دوره حقوق", max_length=20, help_text="مثال: 1405-04")
    base_rial = models.BigIntegerField("حقوق پایه (ریال)", default=0)
    benefits_rial = models.BigIntegerField("مزایا (ریال)", default=0)
    deductions_rial = models.BigIntegerField("کسورات (ریال)", default=0)
    status = models.CharField("وضعیت", max_length=10, choices=STATUS_CHOICES, default=DRAFT)

    class Meta:
        verbose_name = "حقوق و دستمزد"
        verbose_name_plural = "حقوق و دستمزد"
        unique_together = ("employee", "period")
        ordering = ("-period", "employee")

    def __str__(self):
        return f"{self.employee} — {self.period}"

    @property
    def net_pay_rial(self):
        return self.base_rial + self.benefits_rial - self.deductions_rial
