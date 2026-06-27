from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from .env import validate_production_environment


class ProductionEnvironmentValidationTests(SimpleTestCase):
    def test_production_rejects_insecure_secret_key(self):
        with self.assertRaises(ImproperlyConfigured):
            validate_production_environment(
                {"DJANGO_ENV": "production"},
                debug=False,
                secret_key="dev-insecure-change-me",
                allowed_hosts=["olkaa.ir"],
            )

    def test_production_rejects_debug_true(self):
        with self.assertRaises(ImproperlyConfigured):
            validate_production_environment(
                {"DJANGO_ENV": "production"},
                debug=True,
                secret_key="secure-test-secret-key",
                allowed_hosts=["olkaa.ir"],
            )

    def test_production_rejects_wildcard_allowed_hosts(self):
        with self.assertRaises(ImproperlyConfigured):
            validate_production_environment(
                {"DJANGO_ENV": "production"},
                debug=False,
                secret_key="secure-test-secret-key",
                allowed_hosts=["*"],
            )

    def test_development_allows_local_defaults(self):
        validate_production_environment(
            {},
            debug=True,
            secret_key="dev-insecure-change-me",
            allowed_hosts=["*"],
        )
