"""
پنل ادمین واحد مالی.

سند با آرتیکل‌هایش به‌صورت inline ویرایش می‌شود و قبل از ذخیره، تراز بودن
(برابری بدهکار و بستانکار) بررسی می‌شود.
"""
from django import forms
from django.contrib import admin, messages
from django.utils import timezone

from .models import Account, BankAccount, Expense, FiscalYear, Invoice, InvoiceLine, Voucher, VoucherLine


@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date", "is_closed")
    list_filter = ("is_closed",)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "account_type", "parent", "is_active")
    list_filter = ("account_type", "is_active")
    search_fields = ("code", "name")
    autocomplete_fields = ("parent",)
    ordering = ("code",)


class VoucherLineInlineFormSet(forms.BaseInlineFormSet):
    """بررسی تراز سند: جمع بدهکار باید با جمع بستانکار برابر باشد."""

    def clean(self):
        super().clean()
        total_debit = 0
        total_credit = 0
        line_count = 0
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            cd = form.cleaned_data
            if not cd or cd.get("DELETE"):
                continue
            debit = cd.get("debit_rial") or 0
            credit = cd.get("credit_rial") or 0
            if debit and credit:
                raise forms.ValidationError(
                    "هر آرتیکل فقط می‌تواند بدهکار یا بستانکار باشد، نه هر دو."
                )
            if not debit and not credit:
                continue
            total_debit += debit
            total_credit += credit
            line_count += 1
        if line_count and total_debit != total_credit:
            raise forms.ValidationError(
                f"سند تراز نیست: جمع بدهکار {total_debit:,} ≠ جمع بستانکار {total_credit:,} ریال."
            )


class VoucherLineInline(admin.TabularInline):
    model = VoucherLine
    formset = VoucherLineInlineFormSet
    extra = 2
    autocomplete_fields = ("account", "party")


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ("number", "date", "fiscal_year", "description", "is_posted", "balance_display")
    list_filter = ("fiscal_year", "is_posted")
    search_fields = ("number", "description")
    inlines = [VoucherLineInline]

    @admin.display(description="تراز")
    def balance_display(self, obj):
        return "✓ متراز" if obj.is_balanced else "✗ نامتراز"


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("title", "bank_name", "sheba_number", "card_number", "opening_balance_rial", "is_active")
    list_filter = ("bank_name", "is_active")
    search_fields = ("title", "bank_name", "account_number", "sheba_number", "card_number")


class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine
    extra = 1
    fields = ("description", "quantity", "unit_price_rial", "line_total_display")
    readonly_fields = ("line_total_display",)

    @admin.display(description="جمع ردیف")
    def line_total_display(self, obj):
        if not obj.pk:
            return "-"
        return f"{obj.total_rial:,} ریال"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "party",
        "title",
        "issue_date",
        "due_date",
        "status",
        "total_display",
        "tracking_code",
    )
    list_filter = ("status", "issue_date", "due_date")
    search_fields = ("number", "party__name", "title", "tracking_code", "note")
    autocomplete_fields = ("party",)
    inlines = (InvoiceLineInline,)
    actions = ("mark_issued", "mark_paid", "mark_overdue")
    readonly_fields = ("subtotal_display", "total_display", "paid_at", "created_at", "updated_at")
    fieldsets = (
        ("اطلاعات فاکتور", {"fields": ("number", "party", "title", "issue_date", "due_date", "status")}),
        ("مبالغ", {"fields": ("subtotal_display", "discount_rial", "tax_rial", "total_display")}),
        ("پرداخت", {"fields": ("paid_at", "tracking_code")}),
        ("توضیحات", {"fields": ("note",)}),
        ("زمان‌ها", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="جمع قبل از تخفیف")
    def subtotal_display(self, obj):
        if not obj.pk:
            return "-"
        return f"{obj.subtotal_rial:,} ریال"

    @admin.display(description="جمع نهایی")
    def total_display(self, obj):
        if not obj.pk:
            return "-"
        return f"{obj.total_rial:,} ریال"

    @admin.action(description="صدور فاکتورهای انتخابی")
    def mark_issued(self, request, queryset):
        updated = queryset.update(status=Invoice.ISSUED)
        self.message_user(request, f"{updated} فاکتور صادر شد.", messages.SUCCESS)

    @admin.action(description="ثبت پرداخت فاکتورهای انتخابی")
    def mark_paid(self, request, queryset):
        updated = queryset.update(status=Invoice.PAID, paid_at=timezone.now())
        self.message_user(request, f"{updated} فاکتور پرداخت شده ثبت شد.", messages.SUCCESS)

    @admin.action(description="علامت‌گذاری سررسید گذشته")
    def mark_overdue(self, request, queryset):
        updated = queryset.update(status=Invoice.OVERDUE)
        self.message_user(request, f"{updated} فاکتور سررسید گذشته شد.", messages.WARNING)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("date", "title", "category", "party", "bank_account", "amount_rial", "status", "paid_at")
    list_filter = ("status", "category", "date", "bank_account")
    search_fields = ("title", "category", "party__name", "tracking_code", "note")
    autocomplete_fields = ("party", "bank_account")
    readonly_fields = ("paid_at", "created_at", "updated_at")
    actions = ("mark_approved", "mark_paid", "mark_rejected")
    fieldsets = (
        ("هزینه", {"fields": ("date", "title", "category", "party", "amount_rial", "status")}),
        ("پرداخت", {"fields": ("bank_account", "paid_at", "tracking_code")}),
        ("توضیحات", {"fields": ("note",)}),
        ("زمان‌ها", {"fields": ("created_at", "updated_at")}),
    )

    @admin.action(description="تایید هزینه‌های انتخابی")
    def mark_approved(self, request, queryset):
        updated = queryset.update(status=Expense.APPROVED)
        self.message_user(request, f"{updated} هزینه تایید شد.", messages.SUCCESS)

    @admin.action(description="ثبت پرداخت هزینه‌های انتخابی")
    def mark_paid(self, request, queryset):
        updated = queryset.update(status=Expense.PAID, paid_at=timezone.now())
        self.message_user(request, f"{updated} هزینه پرداخت شد.", messages.SUCCESS)

    @admin.action(description="رد هزینه‌های انتخابی")
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status=Expense.REJECTED)
        self.message_user(request, f"{updated} هزینه رد شد.", messages.WARNING)
