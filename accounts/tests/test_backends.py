from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.backends import EmailBackend

User = get_user_model()

class EmailBackendTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="Admin123@"
        )
        self.backend = EmailBackend()

    def test_authenticate_with_email(self):
        user = self.backend.authenticate(
            request=None,
            username="test@example.com",
            password="Admin123@"
        )
        self.assertIsNotNone(user)

    def test_authenticate_invalid(self):
        user = self.backend.authenticate(
            request=None,
            username="wrong@example.com",
            password="wrong"
        )
        self.assertIsNone(user)
