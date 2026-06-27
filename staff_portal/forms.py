from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from hr.models import StaffRegistrationRequest


class RegistrationCodeForm(forms.Form):
    registration_code = forms.CharField(label="رمز ثبت‌نام داخلی", widget=forms.PasswordInput)

    def clean_registration_code(self):
        registration_code = self.cleaned_data["registration_code"]
        expected_code = getattr(settings, "STAFF_REGISTRATION_CODE", "")
        if expected_code and registration_code != expected_code:
            raise ValidationError("رمز ثبت‌نام داخلی درست نیست.")
        return registration_code


class EmailOtpForm(forms.Form):
    code = forms.CharField(
        label="کد ورود ایمیل",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "one-time-code",
                "inputmode": "numeric",
                "pattern": "[0-9]*",
            }
        ),
    )

    def clean_code(self):
        code = "".join(ch for ch in self.cleaned_data["code"] if ch.isdigit())
        if len(code) != 6:
            raise ValidationError("کد ورود باید ۶ رقم باشد.")
        return code


class StaffLoginForm(AuthenticationForm):
    username = forms.CharField(label="ایمیل یا نام کاربری")
    password = forms.CharField(label="رمز عبور", strip=False, widget=forms.PasswordInput)


class StaffRegistrationForm(forms.Form):
    first_name = forms.CharField(label="نام", max_length=150)
    last_name = forms.CharField(label="نام خانوادگی", max_length=150)
    email = forms.EmailField(label="ایمیل")
    mobile = forms.CharField(label="موبایل", max_length=15, required=False)
    national_id = forms.CharField(label="کد ملی", max_length=10, required=False)
    requested_department = forms.CharField(label="واحد", max_length=80, required=False)
    requested_job_title = forms.CharField(label="عنوان شغلی", max_length=120, required=False)
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput)

    allowed_domains = ("olkaa.ir", "gmail.com")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        domain = email.rsplit("@", 1)[-1]
        if domain not in self.allowed_domains:
            raise ValidationError("ثبت‌نام فعلا با ایمیل olkaa.ir یا Gmail مجاز است.")
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
            requested_ticketing=True,
        )
