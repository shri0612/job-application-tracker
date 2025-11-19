from django.test import TestCase
from accounts.utils import validate_password_strength

class UtilsTest(TestCase):
    def test_strong_password(self):
        result = validate_password_strength("Admin123@")
        self.assertTrue(result)

    def test_weak_password(self):
        with self.assertRaises(ValueError):
            validate_password_strength("weak")
