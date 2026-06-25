"""اعتبارسنج‌های اختصاصی ایران."""
from django.core.exceptions import ValidationError


def validate_national_id(value):
    """اعتبارسنجی کد ملی ایران (۱۰ رقمی، با رقم کنترلی)."""
    if not value:
        return
    code = str(value).strip()
    if not code.isdigit() or len(code) != 10:
        raise ValidationError("کد ملی باید ۱۰ رقم باشد.")
    if code == code[0] * 10:
        raise ValidationError("کد ملی نامعتبر است.")
    checksum = sum(int(code[i]) * (10 - i) for i in range(9))
    remainder = checksum % 11
    control = int(code[9])
    valid = (remainder < 2 and control == remainder) or (
        remainder >= 2 and control == 11 - remainder
    )
    if not valid:
        raise ValidationError("کد ملی نامعتبر است.")
