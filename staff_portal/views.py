from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    modules = [
        {
            "title": "واحد مالی",
            "caption": "کدینگ، اسناد، پرداخت‌ها و گزارش‌های مالی",
            "href": "/admin/accounting/",
            "status": "فعال",
        },
        {
            "title": "منابع انسانی",
            "caption": "پرونده پرسنلی، حضور و غیاب، مرخصی و حقوق",
            "href": "/admin/hr/",
            "status": "مرحله اول",
        },
        {
            "title": "تیکتینگ",
            "caption": "ارسال درخواست، ارجاع، اولویت‌بندی و پیگیری",
            "href": "/admin/ticketing/",
            "status": "مرحله اول",
        },
        {
            "title": "دیتاسنتر",
            "caption": "پلن‌ها، اشتراک‌ها، بلوک‌های IP و اجاره IP",
            "href": "/admin/datacenter/",
            "status": "مرحله اول",
        },
        {
            "title": "مدیریت کاربران",
            "caption": "کاربران، نقش‌ها، طرف‌حساب‌ها و دسترسی‌ها",
            "href": "/admin/core/",
            "status": "فعال",
        },
    ]
    return render(request, "staff_portal/dashboard.html", {"modules": modules})
