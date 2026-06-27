from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import Role
from .access import user_can_access_module
from .security import OTP_CODE_HASH, OTP_EXPIRES_AT, OTP_USER_ID


@override_settings(
    EMAIL_OTP_ENABLED=False,
    STAFF_PORTAL_THROTTLE_LIMITS={
        "default": (10, 300),
        "login": (2, 300),
        "otp": (2, 300),
        "otp_resend": (2, 300),
        "registration": (2, 300),
    },
)
class StaffPortalAccessTests(TestCase):
    def setUp(self):
        cache.clear()
        User = get_user_model()
        self.staff_user = User.objects.create_user(
            username="staff@example.com",
            email="staff@example.com",
            password="StrongPass123!",
            is_staff=True,
        )
        self.finance_user = User.objects.create_user(
            username="finance@example.com",
            email="finance@example.com",
            password="StrongPass123!",
            is_staff=True,
        )
        role = Role.objects.create(name="کارشناس مالی", slug="finance-operator")
        self.finance_user.roles.add(role)

    def test_staff_without_module_role_cannot_access_finance(self):
        self.assertFalse(user_can_access_module(self.staff_user, "finance"))
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("staff_portal:finance"))
        self.assertEqual(response.status_code, 403)

    def test_staff_with_finance_role_can_access_finance(self):
        self.assertTrue(user_can_access_module(self.finance_user, "finance"))
        self.client.force_login(self.finance_user)
        response = self.client.get(reverse("staff_portal:finance"))
        self.assertEqual(response.status_code, 200)

    def test_staff_without_module_role_cannot_access_datacenter_live_view(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("staff_portal:live"))
        self.assertEqual(response.status_code, 403)


@override_settings(
    EMAIL_OTP_ENABLED=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    STAFF_PORTAL_THROTTLE_LIMITS={
        "default": (10, 300),
        "login": (2, 300),
        "otp": (2, 300),
        "otp_resend": (1, 300),
        "registration": (2, 300),
    },
)
class StaffPortalThrottleTests(TestCase):
    def setUp(self):
        cache.clear()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="StrongPass123!",
            is_staff=True,
        )

    def test_login_throttle_blocks_repeated_failures(self):
        url = reverse("staff_portal:login")
        payload = {"username": self.user.username, "password": "wrong"}
        self.client.post(url, payload, REMOTE_ADDR="10.0.0.1")
        self.client.post(url, payload, REMOTE_ADDR="10.0.0.1")
        response = self.client.post(url, payload, REMOTE_ADDR="10.0.0.1")
        self.assertContains(response, "درخواست‌های زیادی", status_code=200)

    def test_otp_throttle_blocks_repeated_failures(self):
        self.client.force_login(self.user)
        session = self.client.session
        session[OTP_USER_ID] = self.user.pk
        session[OTP_CODE_HASH] = "not-a-real-hash"
        session[OTP_EXPIRES_AT] = 4102444800
        session.save()

        url = reverse("staff_portal:email_otp")
        self.client.post(url, {"code": "111111"}, REMOTE_ADDR="10.0.0.2")
        self.client.post(url, {"code": "222222"}, REMOTE_ADDR="10.0.0.2")
        response = self.client.post(url, {"code": "333333"}, REMOTE_ADDR="10.0.0.2")
        self.assertContains(response, "درخواست‌های زیادی", status_code=200)

    def test_otp_resend_throttle_blocks_repeated_resends(self):
        self.client.force_login(self.user)
        url = reverse("staff_portal:email_otp")
        self.client.post(url, {"action": "resend"}, REMOTE_ADDR="10.0.0.3")
        response = self.client.post(url, {"action": "resend"}, REMOTE_ADDR="10.0.0.3", follow=True)
        self.assertContains(response, "درخواست‌های زیادی", status_code=200)
