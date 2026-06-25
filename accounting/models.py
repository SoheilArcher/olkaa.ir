"""
ماژول حسابداری دوطرفه.

ساختار استاندارد: حساب‌ها (کدینگ درختی) → سند → آرتیکل سند.
قانون تراز: جمع بدهکار هر سند باید با جمع بستانکارش برابر باشد.
مبالغ به ریال و به‌صورت عدد صحیح ذخیره می‌شوند (هیچ‌وقت اعشاری برای پول).
"""
from django.db import models

from core.models import TimeStamped, Party


class FiscalYear(TimeStamped):
    """سال مالی."""

    title = models.CharField("عنوان", max_length=50)
    start_date = models.DateField("تاریخ شروع")
    end_date = models.DateField("تاریخ پایان")
    is_closed = models.BooleanField("بسته‌شده", default=False)

    class Meta:
        verbose_name = "سال مالی"
        verbose_name_plural = "سال‌های مالی"
        ordering = ["-start_date"]

    def __str__(self):
        return self.title


class Account(TimeStamped):
    """حساب (کدینگ). ساختار درختی با والد."""

    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    INCOME = "income"
    EXPENSE = "expense"
    TYPE_CHOICES = [
        (ASSET, "دارایی"),
        (LIABILITY, "بدهی"),
        (EQUITY, "سرمایه"),
        (INCOME, "درآمد"),
        (EXPENSE, "هزینه"),
    ]

    code = models.CharField("کد حساب", max_length=20, unique=True)
    name = models.CharField("نام حساب", max_length=120)
    account_type = models.CharField("نوع", max_length=10, choices=TYPE_CHOICES)
    parent = models.ForeignKey(
        "self",
        verbose_name="حساب والد",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
    )
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "حساب"
        verbose_name_plural = "حساب‌ها (کدینگ)"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} — {self.name}"


class Voucher(TimeStamped):
    """سند حسابداری (سرفصل هر رویداد مالی)."""

    number = models.PositiveIntegerField("شماره سند")
    date = models.DateField("تاریخ")
    fiscal_year = models.ForeignKey(
        FiscalYear, verbose_name="سال مالی", on_delete=models.PROTECT, related_name="vouchers"
    )
    description = models.CharField("شرح", max_length=255, blank=True)
    is_posted = models.BooleanField("ثبت قطعی", default=False)

    class Meta:
        verbose_name = "سند"
        verbose_name_plural = "اسناد"
        ordering = ["-date", "-number"]
        unique_together = ("fiscal_year", "number")

    def __str__(self):
        return f"سند {self.number} — {self.date}"

    @property
    def total_debit(self):
        return sum(line.debit_rial for line in self.lines.all())

    @property
    def total_credit(self):
        return sum(line.credit_rial for line in self.lines.all())

    @property
    def is_balanced(self):
        td, tc = self.total_debit, self.total_credit
        return td == tc and td > 0


class VoucherLine(TimeStamped):
    """آرتیکل سند: یک حساب را بدهکار یا بستانکار می‌کند."""

    voucher = models.ForeignKey(
        Voucher, verbose_name="سند", on_delete=models.CASCADE, related_name="lines"
    )
    account = models.ForeignKey(
        Account, verbose_name="حساب", on_delete=models.PROTECT, related_name="lines"
    )
    party = models.ForeignKey(
        Party,
        verbose_name="طرف‌حساب",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="voucher_lines",
    )
    debit_rial = models.BigIntegerField("بدهکار (ریال)", default=0)
    credit_rial = models.BigIntegerField("بستانکار (ریال)", default=0)
    description = models.CharField("شرح", max_length=255, blank=True)

    class Meta:
        verbose_name = "آرتیکل سند"
        verbose_name_plural = "آرتیکل‌های سند"

    def __str__(self):
        return f"{self.account} — بد {self.debit_rial} / بس {self.credit_rial}"
