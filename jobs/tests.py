from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from jobs.models import Job

class JobTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")

        self.job = Job.objects.create(
            user=self.user,
            title="Software Engineer",
            company="TestCorp",
            status="Applied"
        )

    def test_job_list_loads(self):
        response = self.client.get(reverse("job_list"))
        self.assertEqual(response.status_code, 200)

    def test_add_job(self):
        response = self.client.post(reverse("add_job"), {
            "title": "DevOps Engineer",
            "company": "CloudTech",
            "status": "Applied"
        })
        self.assertEqual(response.status_code, 302)

    def test_edit_job(self):
        response = self.client.post(reverse("edit_job", args=[self.job.id]), {
            "title": "Updated Title",
            "company": "UpdatedCorp",
            "status": "Applied"
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_job(self):
        response = self.client.post(reverse("delete_job", args=[self.job.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Job.objects.filter(id=self.job.id).exists())
