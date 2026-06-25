# فاوا ایمن اُلکا — سامانه‌ی یکپارچه

اسکلت اولیه‌ی پروژه با جنگو. این نسخه شامل هسته‌ی مشترک (`core`) و سایت عمومی
معرفی شرکت (`website`) است و به‌صورت پیش‌فرض با SQLite بالا می‌آید (بدون نیاز به نصب
پایگاه داده).

## راه‌اندازی روی اوبونتو

```bash
# ۱) پیش‌نیازها
sudo apt update
sudo apt install -y python3 python3-venv python3-pip

# ۲) محیط مجازی
cd fava
python3 -m venv .venv
source .venv/bin/activate

# ۳) نصب وابستگی‌ها
pip install --upgrade pip
pip install -r requirements.txt

# ۴) تنظیمات محیط
cp .env.example .env
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(50))"   # خروجی را در .env بگذارید

# ۵) دیتابیس و ادمین
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# ۶) اجرا
python manage.py runserver
```

سپس:
- سایت: http://127.0.0.1:8000
- پنل ادمین: http://127.0.0.1:8000/admin

## ساختار فعلی

```
fava/
├── config/        تنظیمات، urls، wsgi/asgi
├── core/          هسته‌ی مشترک: User, Role, Party, Payment + اعتبارسنج کد ملی
├── website/       سایت عمومی (صفحه‌ی فرود)
├── templates/     base.html و website/home.html
└── static/css/    site.css (پالت سرمه‌ای/طلایی، RTL)
```

## استفاده از PostgreSQL (اختیاری)

```bash
sudo apt install -y postgresql libpq-dev
sudo -u postgres psql -c "CREATE USER fava WITH PASSWORD 'secret';"
sudo -u postgres psql -c "CREATE DATABASE fava OWNER fava;"
# سپس بخش POSTGRES_* را در .env پر کنید و:
pip install psycopg2-binary
python manage.py migrate
```

## قدم‌های بعدی (ماژول‌ها)

به‌ترتیب اولویت ساخته می‌شوند، هرکدام یک اپ جنگو روی همان هسته:

1. `crm` — Lead, Pipeline, Stage, Activity
2. `accounting` — Account, Invoice, Payment, مؤدیان
3. `hr` — Employee, Attendance, Leave, Payroll
4. `ticketing` — Ticket, TicketMessage, SLA
5. `datacenter` — Plan, Subscription + IPBlock, IPLease (IPAM)
6. `portal` — پورتال مشتری (خرید، تمدید، فاکتورها)

ساخت یک اپ جدید:
```bash
python manage.py startapp crm
# سپس "crm" را به INSTALLED_APPS در config/settings.py اضافه کنید
```
