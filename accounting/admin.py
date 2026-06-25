"""
پنل ادمین واحد مالی.

سند با آرتیکل‌هایش به‌صورت inline ویرایش می‌شود و قبل از ذخیره، تراز بودن
(برابری بدهکار و بستانکار) بررسی می‌شود.
"""
from django import forms
from django.contrib import admin

from .models import FiscalYear, Account, Voucher, VoucherLine


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
