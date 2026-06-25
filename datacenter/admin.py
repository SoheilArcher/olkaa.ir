from django.contrib import admin

from .models import IPBlock, IPLease, ServicePlan, Subscription


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
