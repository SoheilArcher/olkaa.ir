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


class BankAccount(TimeStamped):
    """حساب بانکی شرکت برای دریافت/پرداخت."""

    title = models.CharField("عنوان حساب", max_length=120)
    bank_name = models.CharField("نام بانک", max_length=80)
    account_number = models.CharField("شماره حساب", max_length=40, blank=True)
    sheba_number = models.CharField("شماره شبا", max_length=34, blank=True)
    card_number = models.CharField("شماره کارت", max_length=19, blank=True)
    opening_balance_rial = models.BigIntegerField("مانده اولیه (ریال)", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "حساب بانکی"
        verbose_name_plural = "حساب‌های بانکی"
        ordering = ("bank_name", "title")

    def __str__(self):
        return f"{self.title} — {self.bank_name}"


class Invoice(TimeStamped):
    """فاکتور فروش/خدمات."""

    DRAFT = "draft"
    ISSUED = "issued"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELED = "canceled"
    STATUS_CHOICES = [
        (DRAFT, "پیش‌نویس"),
        (ISSUED, "صادر شده"),
        (PAID, "پرداخت شده"),
        (OVERDUE, "سررسید گذشته"),
        (CANCELED, "لغو شده"),
    ]

    number = models.CharField("شماره فاکتور", max_length=40, unique=True)
    party = models.ForeignKey(Party, verbose_name="مشتری/طرف‌حساب", on_delete=models.PROTECT, related_name="invoices")
    title = models.CharField("عنوان", max_length=180)
    issue_date = models.DateField("تاریخ صدور")
    due_date = models.DateField("تاریخ سررسید", null=True, blank=True)
    status = models.CharField("وضعیت", max_length=12, choices=STATUS_CHOICES, default=DRAFT)
    discount_rial = models.BigIntegerField("تخفیف (ریال)", default=0)
    tax_rial = models.BigIntegerField("مالیات/ارزش افزوده (ریال)", default=0)
    paid_at = models.DateTimeField("زمان پرداخت", null=True, blank=True)
    tracking_code = models.CharField("کد پیگیری", max_length=80, blank=True)
    note = models.TextField("توضیح", blank=True)

    class Meta:
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتورها"
        ordering = ("-issue_date", "-number")

    def __str__(self):
        return f"{self.number} — {self.party}"

    @property
    def subtotal_rial(self):
        return sum(line.total_rial for line in self.lines.all())

    @property
    def total_rial(self):
        return max(0, self.subtotal_rial - self.discount_rial + self.tax_rial)


class InvoiceLine(TimeStamped):
    invoice = models.ForeignKey(Invoice, verbose_name="فاکتور", on_delete=models.CASCADE, related_name="lines")
    description = models.CharField("شرح", max_length=255)
    quantity = models.PositiveIntegerField("تعداد", default=1)
    unit_price_rial = models.BigIntegerField("مبلغ واحد (ریال)", default=0)

    class Meta:
        verbose_name = "ردیف فاکتور"
        verbose_name_plural = "ردیف‌های فاکتور"

    def __str__(self):
        return f"{self.description} — {self.total_rial:,} ریال"

    @property
    def total_rial(self):
        return self.quantity * self.unit_price_rial


class Expense(TimeStamped):
    """هزینه/پرداخت عملیاتی."""

    PENDING = "pending"
    APPROVED = "approved"
    PAID = "paid"
    REJECTED = "rejected"
    STATUS_CHOICES = [
        (PENDING, "در انتظار"),
        (APPROVED, "تایید شده"),
        (PAID, "پرداخت شده"),
        (REJECTED, "رد شده"),
    ]

    date = models.DateField("تاریخ")
    title = models.CharField("عنوان هزینه", max_length=180)
    category = models.CharField("دسته", max_length=80, blank=True)
    party = models.ForeignKey(Party, verbose_name="طرف‌حساب", on_delete=models.SET_NULL, null=True, blank=True)
    bank_account = models.ForeignKey(
        BankAccount, verbose_name="حساب پرداخت", on_delete=models.SET_NULL, null=True, blank=True
    )
    amount_rial = models.BigIntegerField("مبلغ (ریال)")
    status = models.CharField("وضعیت", max_length=12, choices=STATUS_CHOICES, default=PENDING)
    paid_at = models.DateTimeField("زمان پرداخت", null=True, blank=True)
    tracking_code = models.CharField("کد پیگیری", max_length=80, blank=True)
    note = models.TextField("توضیح", blank=True)

    class Meta:
        verbose_name = "هزینه"
        verbose_name_plural = "هزینه‌ها"
        ordering = ("-date", "-created_at")

    def __str__(self):
        return f"{self.title} — {self.amount_rial:,} ریال"
