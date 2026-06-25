from django.contrib import admin

from .management.commands.check_ping_targets import check_target
from .models import IPBlock, IPLease, PingCheck, PingTarget, ServicePlan, Subscription


@admin.register(ServicePlan)
class ServicePlanAdmin(admin.ModelAdmin):
    list_display = ("title", "service_type", "bandwidth_mbps", "monthly_price_rial", "is_active")
    list_filter = ("service_type", "is_active")
    search_fields = ("title",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("party", "plan", "status", "start_date", "end_date", "circuit_id")
    list_filter = ("status", "plan__service_type", "start_date", "end_date")
    search_fields = ("party__name", "plan__title", "circuit_id")
    autocomplete_fields = ("party", "plan")


@admin.register(IPBlock)
class IPBlockAdmin(admin.ModelAdmin):
    list_display = ("cidr", "owner", "total_addresses", "is_available")
    list_filter = ("is_available", "owner")
    search_fields = ("cidr", "owner", "note")


@admin.register(IPLease)
class IPLeaseAdmin(admin.ModelAdmin):
    list_display = ("assigned_cidr", "block", "party", "status", "start_date", "end_date")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("assigned_cidr", "block__cidr", "party__name")
    autocomplete_fields = ("block", "party")


@admin.register(PingTarget)
class PingTargetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "host",
        "target_type",
        "environment",
        "support_owner",
        "alert_emails",
        "last_status",
        "last_latency_ms",
        "failure_count",
        "last_checked_at",
        "is_active",
    )
    list_filter = ("last_status", "target_type", "environment", "is_active", "last_checked_at")
    search_fields = ("name", "host", "support_owner", "support_hint", "note")
    fieldsets = (
        ("شناسه سرویس", {"fields": ("name", "host", "target_type", "environment", "is_active")}),
        ("پشتیبانی", {"fields": ("support_owner", "support_hint", "alert_emails", "note")}),
        (
            "آخرین وضعیت",
            {
                "fields": ("last_status", "last_latency_ms", "failure_count", "last_checked_at", "last_alert_sent_at"),
            },
        ),
    )
    readonly_fields = ("last_status", "last_latency_ms", "failure_count", "last_checked_at", "last_alert_sent_at")
    actions = ("run_ping_check",)

    @admin.action(description="اجرای پینگ برای سرویس‌های انتخابی")
    def run_ping_check(self, request, queryset):
        for target in queryset:
            check_target(target)


@admin.register(PingCheck)
class PingCheckAdmin(admin.ModelAdmin):
    list_display = ("target", "status", "latency_ms", "status_changed", "alert_sent_at", "created_at")
    list_filter = ("status", "status_changed", "alert_sent_at", "created_at", "target")
    search_fields = ("target__name", "target__host", "output")
    autocomplete_fields = ("target",)
    readonly_fields = ("created_at", "updated_at", "alert_sent_at")
