from django.contrib import admin

from .models import Attendance, EmployeeProfile, Payroll


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("personnel_code", "user", "department", "job_title", "base_salary_rial", "status")
    list_filter = ("department", "status", "hire_date")
    search_fields = ("personnel_code", "user__username", "user__first_name", "user__last_name", "job_title")
    autocomplete_fields = ("user",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "check_in", "check_out", "status")
    list_filter = ("status", "date")
    search_fields = ("employee__personnel_code", "employee__user__username", "employee__user__first_name")
    autocomplete_fields = ("employee",)
    date_hierarchy = "date"


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ("employee", "period", "base_rial", "benefits_rial", "deductions_rial", "net_pay_display", "status")
    list_filter = ("status", "period")
    search_fields = ("employee__personnel_code", "employee__user__username", "period")
    autocomplete_fields = ("employee",)

    @admin.display(description="خالص پرداختی")
    def net_pay_display(self, obj):
        return f"{obj.net_pay_rial:,} ریال"
