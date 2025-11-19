from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class JobViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Admin123@"
        )
        self.client.login(username="test@example.com", password="Admin123@")

    def test_job_list(self):
        response = self.client.get(reverse("job_list"))
        self.assertEqual(response.status_code, 200)

    def test_add_job_page(self):
        response = self.client.get(reverse("add_job"))
        self.assertEqual(response.status_code, 200)
