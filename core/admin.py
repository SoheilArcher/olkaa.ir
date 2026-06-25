from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Role, Party, User, Payment


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("name", "party_type", "national_id", "mobile", "is_customer")
    list_filter = ("party_type", "is_customer")
    search_fields = ("name", "national_id", "economic_code", "mobile", "email")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("party", "amount_rial", "status", "gateway", "created_at")
    list_filter = ("status", "gateway")
    search_fields = ("party__name", "authority", "ref_id")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (("اطلاعات فاوا", {"fields": ("party", "roles")}),)
    filter_horizontal = BaseUserAdmin.filter_horizontal + ("roles",)
