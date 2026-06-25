import csv

from django.contrib import admin, messages
from django.contrib.auth.models import Permission
from django.http import HttpResponse
from django.utils import timezone

from core.models import Role

from .models import Attendance, EmployeeProfile, Payroll, StaffRegistrationRequest


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = (
        "personnel_code",
        "user",
        "department",
        "job_title",
        "base_salary_rial",
        "bank_name",
        "sheba_number",
        "status",
    )
    list_filter = ("department", "status", "hire_date")
    search_fields = (
        "personnel_code",
        "user__username",
        "user__first_name",
        "user__last_name",
        "job_title",
        "bank_name",
        "sheba_number",
        "bank_account_number",
    )
    autocomplete_fields = ("user",)
    fieldsets = (
        ("اطلاعات پرسنلی", {"fields": ("user", "personnel_code", "department", "job_title", "hire_date", "status")}),
        ("حقوق", {"fields": ("base_salary_rial", "payroll_note")}),
        ("اطلاعات بانکی", {"fields": ("bank_name", "bank_account_number", "sheba_number", "card_number")}),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "check_in", "check_out", "status")
    list_filter = ("status", "date")
    search_fields = ("employee__personnel_code", "employee__user__username", "employee__user__first_name")
    autocomplete_fields = ("employee",)
    date_hierarchy = "date"


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "period",
        "base_rial",
        "benefits_rial",
        "deductions_rial",
        "net_pay_display",
        "status",
        "paid_at",
        "bank_tracking_code",
    )
    list_filter = ("status", "period", "paid_at")
    search_fields = (
        "employee__personnel_code",
        "employee__user__username",
        "employee__user__first_name",
        "employee__user__last_name",
        "period",
        "bank_tracking_code",
    )
    autocomplete_fields = ("employee",)
    actions = ("mark_approved", "mark_paid", "export_bank_payment_csv")

    @admin.display(description="خالص پرداختی")
    def net_pay_display(self, obj):
        return f"{obj.net_pay_rial:,} ریال"

    @admin.action(description="تایید فیش‌های انتخابی")
    def mark_approved(self, request, queryset):
        updated = queryset.update(status=Payroll.APPROVED)
        self.message_user(request, f"{updated} فیش تایید شد.", messages.SUCCESS)

    @admin.action(description="ثبت پرداخت فیش‌های انتخابی")
    def mark_paid(self, request, queryset):
        updated = queryset.update(status=Payroll.PAID, paid_at=timezone.now())
        self.message_user(request, f"{updated} فیش به عنوان پرداخت شده ثبت شد.", messages.SUCCESS)

    @admin.action(description="خروجی CSV پرداخت بانکی")
    def export_bank_payment_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="payroll-bank-export.csv"'
        response.write("\ufeff")
        writer = csv.writer(response)
        writer.writerow(["period", "employee", "national_id", "bank", "sheba", "account", "card", "amount_rial"])
        for payroll in queryset.select_related("employee", "employee__user"):
            employee = payroll.employee
            writer.writerow(
                [
                    payroll.period,
                    employee.user.get_full_name() or employee.user.username,
                    getattr(employee.user, "staff_registration", None).national_id
                    if hasattr(employee.user, "staff_registration")
                    else "",
                    employee.bank_name,
                    employee.sheba_number,
                    employee.bank_account_number,
                    employee.card_number,
                    payroll.net_pay_rial,
                ]
            )
        return response


@admin.register(StaffRegistrationRequest)
class StaffRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "mobile",
        "requested_department",
        "requested_job_title",
        "requested_accesses",
        "status",
        "email_verified_at",
        "approved_by",
        "created_at",
    )
    list_filter = (
        "status",
        "requested_finance",
        "requested_hr",
        "requested_attendance",
        "requested_payroll",
        "requested_ticketing",
        "requested_datacenter",
        "requested_user_manager",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "mobile",
        "national_id",
        "requested_department",
        "requested_job_title",
    )
    autocomplete_fields = ("user", "approved_by")
    readonly_fields = ("created_at", "updated_at", "email_verified_at", "approved_at")
    actions = ("approve_requests", "reject_requests")
    fieldsets = (
        ("درخواست", {"fields": ("user", "status", "mobile", "national_id", "requested_department", "requested_job_title")}),
        (
            "دسترسی‌های درخواستی",
            {
                "fields": (
                    "requested_finance",
                    "requested_hr",
                    "requested_attendance",
                    "requested_payroll",
                    "requested_ticketing",
                    "requested_datacenter",
                    "requested_user_manager",
                )
            },
        ),
        ("تایید", {"fields": ("email_verified_at", "approved_at", "approved_by", "manager_note")}),
        ("زمان‌ها", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="دسترسی‌ها")
    def requested_accesses(self, obj):
        return obj.requested_accesses_display

    def _role(self, name, slug):
        role, _ = Role.objects.get_or_create(slug=slug, defaults={"name": name})
        return role

    def _apply_roles(self, registration):
        role_map = [
            (
                registration.requested_finance,
                "کارشناس مالی",
                "finance-operator",
                {
                    ("accounting", "view_account"),
                    ("accounting", "view_voucher"),
                    ("accounting", "change_voucher"),
                    ("core", "view_payment"),
                    ("core", "change_payment"),
                    ("core", "view_party"),
                },
            ),
            (
                registration.requested_hr,
                "منابع انسانی",
                "hr-operator",
                {
                    ("hr", "view_employeeprofile"),
                    ("hr", "change_employeeprofile"),
                    ("hr", "view_staffregistrationrequest"),
                },
            ),
            (
                registration.requested_attendance,
                "حضور و غیاب",
                "attendance-operator",
                {
                    ("hr", "view_attendance"),
                    ("hr", "add_attendance"),
                    ("hr", "change_attendance"),
                },
            ),
            (
                registration.requested_payroll,
                "حقوق و دستمزد",
                "payroll-operator",
                {
                    ("hr", "view_payroll"),
                    ("hr", "add_payroll"),
                    ("hr", "change_payroll"),
                },
            ),
            (
                registration.requested_ticketing,
                "تیکتینگ",
                "ticket-operator",
                {
                    ("ticketing", "view_ticket"),
                    ("ticketing", "add_ticket"),
                    ("ticketing", "change_ticket"),
                    ("ticketing", "view_ticketreply"),
                    ("ticketing", "add_ticketreply"),
                    ("ticketing", "change_ticketreply"),
                },
            ),
            (
                registration.requested_datacenter,
                "کارشناس دیتاسنتر",
                "datacenter-operator",
                {
                    ("datacenter", "view_serviceplan"),
                    ("datacenter", "view_subscription"),
                    ("datacenter", "change_subscription"),
                    ("datacenter", "view_ipblock"),
                    ("datacenter", "view_iplease"),
                    ("datacenter", "view_pingtarget"),
                    ("datacenter", "add_pingtarget"),
                    ("datacenter", "change_pingtarget"),
                    ("datacenter", "view_pingcheck"),
                },
            ),
            (
                registration.requested_user_manager,
                "مدیریت کاربران",
                "user-manager",
                {
                    ("core", "view_user"),
                    ("core", "change_user"),
                    ("core", "view_role"),
                    ("core", "change_role"),
                    ("hr", "view_staffregistrationrequest"),
                    ("hr", "change_staffregistrationrequest"),
                },
            ),
        ]
        for enabled, name, slug, permissions in role_map:
            if enabled:
                registration.user.roles.add(self._role(name, slug))
                for app_label, codename in permissions:
                    permission = Permission.objects.filter(
                        content_type__app_label=app_label,
                        codename=codename,
                    ).first()
                    if permission:
                        registration.user.user_permissions.add(permission)

    @admin.action(description="تایید کارمند و فعال‌سازی دسترسی‌ها")
    def approve_requests(self, request, queryset):
        approved = 0
        for registration in queryset.select_related("user"):
            registration.user.is_active = True
            registration.user.is_staff = True
            registration.user.save(update_fields=("is_active", "is_staff"))
            self._apply_roles(registration)
            EmployeeProfile.objects.get_or_create(
                user=registration.user,
                defaults={
                    "personnel_code": f"EMP-{registration.user_id:05d}",
                    "department": registration.requested_department,
                    "job_title": registration.requested_job_title,
                },
            )
            registration.status = StaffRegistrationRequest.APPROVED
            registration.approved_at = timezone.now()
            registration.approved_by = request.user
            registration.save(update_fields=("status", "approved_at", "approved_by", "updated_at"))
            approved += 1
        self.message_user(request, f"{approved} درخواست تایید و کاربرها فعال شدند.", messages.SUCCESS)

    @admin.action(description="رد درخواست‌های انتخابی")
    def reject_requests(self, request, queryset):
        updated = queryset.update(status=StaffRegistrationRequest.REJECTED)
        self.message_user(request, f"{updated} درخواست رد شد.", messages.WARNING)
