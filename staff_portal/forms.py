from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from hr.models import StaffRegistrationRequest


class StaffRegistrationForm(forms.Form):
    first_name = forms.CharField(label="نام", max_length=150)
    last_name = forms.CharField(label="نام خانوادگی", max_length=150)
    email = forms.EmailField(label="ایمیل سازمانی")
    mobile = forms.CharField(label="موبایل", max_length=15, required=False)
    national_id = forms.CharField(label="کد ملی", max_length=10, required=False)
    requested_department = forms.CharField(label="واحد", max_length=80, required=False)
    requested_job_title = forms.CharField(label="عنوان شغلی", max_length=120, required=False)
    registration_code = forms.CharField(label="رمز ثبت‌نام داخلی", widget=forms.PasswordInput)
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput)
    requested_finance = forms.BooleanField(label="واحد مالی", required=False)
    requested_hr = forms.BooleanField(label="منابع انسانی", required=False)
    requested_attendance = forms.BooleanField(label="حضور و غیاب", required=False)
    requested_payroll = forms.BooleanField(label="حقوق و دستمزد", required=False)
    requested_ticketing = forms.BooleanField(label="تیکتینگ", required=False, initial=True)
    requested_datacenter = forms.BooleanField(label="دیتاسنتر", required=False)

    allowed_domains = ("olkaa.ir",)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        domain = email.rsplit("@", 1)[-1]
        if domain not in self.allowed_domains:
            raise ValidationError("فعلا ثبت‌نام فقط با ایمیل سازمانی olkaa.ir مجاز است.")
        User = get_user_model()
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            raise ValidationError("برای این ایمیل قبلا حساب کاربری ثبت شده است.")
        return email

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "رمز عبور و تکرار آن یکسان نیست.")
        if password1:
            try:
                validate_password(password1)
            except ValidationError as error:
                self.add_error("password1", error)
        registration_code = cleaned.get("registration_code")
        expected_code = getattr(settings, "STAFF_REGISTRATION_CODE", "")
        if expected_code and registration_code != expected_code:
            self.add_error("registration_code", "رمز ثبت‌نام داخلی درست نیست.")
        return cleaned

    def save(self):
        User = get_user_model()
        email = self.cleaned_data["email"]
        user = User.objects.create_user(
            username=email,
            email=email,
            password=self.cleaned_data["password1"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            is_active=False,
            is_staff=False,
        )
        return StaffRegistrationRequest.objects.create(
            user=user,
            mobile=self.cleaned_data.get("mobile", ""),
            national_id=self.cleaned_data.get("national_id", ""),
            requested_department=self.cleaned_data.get("requested_department", ""),
            requested_job_title=self.cleaned_data.get("requested_job_title", ""),
            requested_finance=self.cleaned_data.get("requested_finance", False),
            requested_hr=self.cleaned_data.get("requested_hr", False),
            requested_attendance=self.cleaned_data.get("requested_attendance", False),
            requested_payroll=self.cleaned_data.get("requested_payroll", False),
            requested_ticketing=self.cleaned_data.get("requested_ticketing", False),
            requested_datacenter=self.cleaned_data.get("requested_datacenter", False),
        )
