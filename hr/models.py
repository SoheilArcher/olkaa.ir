from django.conf import settings
from django.db import models
from django.utils import timezone

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
    bank_name = models.CharField("نام بانک", max_length=80, blank=True)
    bank_account_number = models.CharField("شماره حساب", max_length=40, blank=True)
    sheba_number = models.CharField("شماره شبا", max_length=34, blank=True)
    card_number = models.CharField("شماره کارت", max_length=19, blank=True)
    payroll_note = models.TextField("توضیح پرداخت حقوق", blank=True)
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
    paid_at = models.DateTimeField("زمان پرداخت", null=True, blank=True)
    bank_tracking_code = models.CharField("کد پیگیری بانکی", max_length=80, blank=True)
    payment_note = models.TextField("توضیح پرداخت", blank=True)

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

    def mark_paid(self, tracking_code=""):
        self.status = self.PAID
        self.paid_at = timezone.now()
        if tracking_code:
            self.bank_tracking_code = tracking_code
        self.save(update_fields=("status", "paid_at", "bank_tracking_code", "updated_at"))


class StaffRegistrationRequest(TimeStamped):
    PENDING_EMAIL = "pending_email"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    STATUS_CHOICES = [
        (PENDING_EMAIL, "در انتظار تایید ایمیل"),
        (PENDING_APPROVAL, "در انتظار تایید مدیر"),
        (APPROVED, "تایید شده"),
        (REJECTED, "رد شده"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="کاربر",
        on_delete=models.CASCADE,
        related_name="staff_registration",
    )
    mobile = models.CharField("موبایل", max_length=15, blank=True)
    national_id = models.CharField("کد ملی", max_length=10, blank=True)
    requested_department = models.CharField("واحد درخواستی", max_length=80, blank=True)
    requested_job_title = models.CharField("عنوان شغلی درخواستی", max_length=120, blank=True)
    requested_finance = models.BooleanField("دسترسی مالی", default=False)
    requested_hr = models.BooleanField("دسترسی منابع انسانی", default=False)
    requested_attendance = models.BooleanField("دسترسی حضور و غیاب", default=False)
    requested_payroll = models.BooleanField("دسترسی حقوق و دستمزد", default=False)
    requested_ticketing = models.BooleanField("دسترسی تیکتینگ", default=True)
    requested_datacenter = models.BooleanField("دسترسی دیتاسنتر", default=False)
    requested_user_manager = models.BooleanField("دسترسی مدیریت کاربران", default=False)
    email_verified_at = models.DateTimeField("زمان تایید ایمیل", null=True, blank=True)
    approved_at = models.DateTimeField("زمان تایید مدیر", null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="تاییدکننده",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_staff_requests",
    )
    status = models.CharField("وضعیت", max_length=20, choices=STATUS_CHOICES, default=PENDING_EMAIL)
    manager_note = models.TextField("یادداشت مدیر", blank=True)

    class Meta:
        verbose_name = "درخواست ثبت‌نام کارمند"
        verbose_name_plural = "درخواست‌های ثبت‌نام کارمندان"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} — {self.get_status_display()}"

    @property
    def requested_accesses_display(self):
        accesses = []
        pairs = [
            (self.requested_finance, "مالی"),
            (self.requested_hr, "منابع انسانی"),
            (self.requested_attendance, "حضور و غیاب"),
            (self.requested_payroll, "حقوق و دستمزد"),
            (self.requested_ticketing, "تیکتینگ"),
            (self.requested_datacenter, "دیتاسنتر"),
            (self.requested_user_manager, "مدیریت کاربران"),
        ]
        for enabled, label in pairs:
            if enabled:
                accesses.append(label)
        return "، ".join(accesses) or "-"
