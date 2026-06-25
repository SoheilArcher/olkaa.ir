from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Role, Party, User, Payment


class PartyUserInline(admin.TabularInline):
    model = User
    fields = ("username", "email", "first_name", "last_name", "is_active", "is_staff", "last_login")
    readonly_fields = ("last_login",)
    extra = 0
    show_change_link = True


class PartyPaymentInline(admin.TabularInline):
    model = Payment
    fields = ("amount_rial", "amount_toman_display", "status", "gateway", "authority", "ref_id", "created_at")
    readonly_fields = ("amount_toman_display", "created_at")
    extra = 0
    show_change_link = True

    @admin.display(description="مبلغ (تومان)")
    def amount_toman_display(self, obj):
        if not obj.pk:
            return "-"
        return f"{obj.amount_toman:,}"


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "party_type",
        "national_id",
        "mobile",
        "email",
        "is_customer",
        "users_count",
        "payments_total_display",
        "updated_at",
    )
    list_filter = ("party_type", "is_customer", "created_at", "updated_at")
    search_fields = ("name", "national_id", "economic_code", "mobile", "email")
    readonly_fields = ("created_at", "updated_at")
    inlines = (PartyUserInline, PartyPaymentInline)
    actions = ("mark_as_customer", "mark_as_not_customer")
    fieldsets = (
        ("اطلاعات اصلی", {"fields": ("party_type", "name", "is_customer")}),
        ("شناسه‌ها", {"fields": ("national_id", "economic_code")}),
        ("راه‌های ارتباطی", {"fields": ("mobile", "email")}),
        ("زمان‌ها", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="کاربران")
    def users_count(self, obj):
        return obj.users.count()

    @admin.display(description="جمع پرداخت موفق")
    def payments_total_display(self, obj):
        total = sum(payment.amount_rial for payment in obj.payments.filter(status=Payment.SUCCESS))
        return f"{total:,} ریال"

    @admin.action(description="تبدیل به مشتری")
    def mark_as_customer(self, request, queryset):
        updated = queryset.update(is_customer=True)
        self.message_user(request, f"{updated} طرف‌حساب به عنوان مشتری علامت خورد.", messages.SUCCESS)

    @admin.action(description="حذف وضعیت مشتری")
    def mark_as_not_customer(self, request, queryset):
        updated = queryset.update(is_customer=False)
        self.message_user(request, f"وضعیت مشتری برای {updated} طرف‌حساب حذف شد.", messages.SUCCESS)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "users_count", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    actions = ("ensure_default_roles",)

    @admin.display(description="تعداد کاربران")
    def users_count(self, obj):
        return obj.users.count()

    @admin.action(description="ساخت نقش‌های پیش‌فرض فاوا")
    def ensure_default_roles(self, request, queryset):
        defaults = [
            ("مدیر سیستم", "system-manager"),
            ("مدیر فروش", "sales-manager"),
            ("کارشناس مالی", "finance-operator"),
            ("کارشناس دیتاسنتر", "datacenter-operator"),
            ("مشتری", "customer"),
        ]
        created = 0
        for name, slug in defaults:
            _, was_created = Role.objects.get_or_create(slug=slug, defaults={"name": name})
            created += int(was_created)
        self.message_user(request, f"{created} نقش جدید ساخته شد؛ نقش‌های موجود دست‌نخورده ماندند.", messages.SUCCESS)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "party",
        "amount_rial",
        "amount_toman_display",
        "status",
        "gateway",
        "authority",
        "ref_id",
        "created_at",
    )
    list_filter = ("status", "gateway", "created_at")
    search_fields = ("party__name", "authority", "ref_id")
    autocomplete_fields = ("party",)
    readonly_fields = ("amount_toman_display", "created_at", "updated_at")
    actions = ("mark_success", "mark_failed", "mark_pending")

    @admin.display(description="مبلغ (تومان)")
    def amount_toman_display(self, obj):
        if not obj.pk:
            return "-"
        return f"{obj.amount_toman:,}"

    @admin.action(description="تغییر وضعیت به موفق")
    def mark_success(self, request, queryset):
        updated = queryset.update(status=Payment.SUCCESS)
        self.message_user(request, f"{updated} پرداخت موفق شد.", messages.SUCCESS)

    @admin.action(description="تغییر وضعیت به ناموفق")
    def mark_failed(self, request, queryset):
        updated = queryset.update(status=Payment.FAILED)
        self.message_user(request, f"{updated} پرداخت ناموفق شد.", messages.WARNING)

    @admin.action(description="تغییر وضعیت به در انتظار")
    def mark_pending(self, request, queryset):
        updated = queryset.update(status=Payment.PENDING)
        self.message_user(request, f"{updated} پرداخت به حالت انتظار برگشت.", messages.INFO)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "full_name_display",
        "email",
        "party",
        "roles_display",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "roles",
        "party__party_type",
        "date_joined",
        "last_login",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "party__name",
        "party__mobile",
        "party__national_id",
        "roles__name",
        "roles__slug",
    )
    list_select_related = ("party",)
    autocomplete_fields = ("party",)
    readonly_fields = ("last_login", "date_joined")
    actions = (
        "activate_users",
        "deactivate_users",
        "make_staff",
        "remove_staff",
        "add_customer_role",
        "add_manager_role",
    )
    fieldsets = (
        ("ورود به سیستم", {"fields": ("username", "password")}),
        ("اطلاعات شخصی", {"fields": ("first_name", "last_name", "email")}),
        ("مدیریت فاوا", {"fields": ("party", "roles")}),
        (
            "وضعیت دسترسی",
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
                "description": "برای دسترسی‌های روزمره از نقش‌ها و صفحه مدیریت داخلی استفاده کنید.",
            },
        ),
        ("زمان‌ها", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            "ساخت کاربر جدید",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                    "party",
                    "roles",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
    filter_horizontal = BaseUserAdmin.filter_horizontal + ("roles",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("roles")

    @admin.display(description="نام کامل")
    def full_name_display(self, obj):
        full_name = obj.get_full_name()
        return full_name or "-"

    @admin.display(description="نقش‌ها")
    def roles_display(self, obj):
        roles = list(obj.roles.all())
        if not roles:
            return "-"
        return "، ".join(role.name for role in roles)

    def _ensure_role(self, name, slug):
        role, _ = Role.objects.get_or_create(slug=slug, defaults={"name": name})
        return role

    @admin.action(description="فعال‌سازی کاربران")
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} کاربر فعال شد.", messages.SUCCESS)

    @admin.action(description="غیرفعال‌سازی کاربران")
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} کاربر غیرفعال شد.", messages.WARNING)

    @admin.action(description="تبدیل به کارمند پنل")
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f"{updated} کاربر دسترسی staff گرفت.", messages.SUCCESS)

    @admin.action(description="حذف دسترسی کارمند پنل")
    def remove_staff(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, f"دسترسی staff برای {updated} کاربر حذف شد.", messages.WARNING)

    @admin.action(description="افزودن نقش مشتری")
    def add_customer_role(self, request, queryset):
        role = self._ensure_role("مشتری", "customer")
        for user in queryset:
            user.roles.add(role)
        self.message_user(request, f"نقش مشتری به {queryset.count()} کاربر اضافه شد.", messages.SUCCESS)

    @admin.action(description="افزودن نقش مدیر سیستم")
    def add_manager_role(self, request, queryset):
        role = self._ensure_role("مدیر سیستم", "system-manager")
        for user in queryset:
            user.roles.add(role)
        self.message_user(request, f"نقش مدیر سیستم به {queryset.count()} کاربر اضافه شد.", messages.SUCCESS)
