from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Admin123@"
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_profile_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)

    def test_profile_logged_in(self):
        self.client.login(username="test@example.com", password="Admin123@")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
