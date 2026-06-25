from django.contrib import admin

from .models import Ticket, TicketReply


class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 1
    autocomplete_fields = ("author",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "requester", "assigned_to", "department", "priority", "status", "created_at")
    list_filter = ("status", "priority", "department", "created_at")
    search_fields = ("title", "description", "requester__username", "assigned_to__username", "party__name")
    autocomplete_fields = ("requester", "assigned_to", "party")
    inlines = (TicketReplyInline,)
    actions = ("mark_in_progress", "mark_closed")

    @admin.action(description="تغییر وضعیت به در حال بررسی")
    def mark_in_progress(self, request, queryset):
        queryset.update(status=Ticket.IN_PROGRESS)

    @admin.action(description="بستن تیکت‌ها")
    def mark_closed(self, request, queryset):
        queryset.update(status=Ticket.CLOSED)


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author", "is_internal", "created_at")
    list_filter = ("is_internal", "created_at")
    search_fields = ("ticket__title", "author__username", "message")
    autocomplete_fields = ("ticket", "author")
