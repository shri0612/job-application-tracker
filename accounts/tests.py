from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        response = self.client.post(reverse("login"), {
            "email": "test@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 302)   # Redirect to job_list

    def test_user_cannot_access_profile_without_login(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_user_can_access_profile_after_login(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
