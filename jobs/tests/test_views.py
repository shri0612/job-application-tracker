import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from jobs.models import Job

@pytest.mark.django_db
def test_job_list_page_loads(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    Job.objects.create(
        title="Test Job",
        company="Test Company",
        location="Dublin",
        status="Applied",
        user=user
    )

    response = client.get(reverse("job_list"))

    assert response.status_code == 200
    assert b"Test Job" in response.content


@pytest.mark.django_db
def test_add_job_creates_entry(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    job_data = {
        "title": "Backend Developer",
        "company": "Google",
        "location": "Remote",
        "status": "Applied",
    }

    response = client.post(reverse("add_job"), job_data)

    assert response.status_code == 302
    assert Job.objects.filter(title="Backend Developer", user=user).exists()


@pytest.mark.django_db
def test_edit_job_updates_entry(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    job = Job.objects.create(
        title="Old Title",
        company="Test",
        location="Test",
        status="Applied",
        user=user
    )

    updated_data = {
        "title": "New Title",
        "company": "Test",
        "location": "Test",
        "status": "Interview",
    }

    response = client.post(reverse("edit_job", args=[job.id]), updated_data)

    assert response.status_code == 302
    job.refresh_from_db()
    assert job.title == "New Title"
    assert job.status == "Interview"


@pytest.mark.django_db
def test_delete_job_removes_entry(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    job = Job.objects.create(
        title="Delete Me",
        company="Test",
        location="Test",
        status="Applied",
        user=user
    )

    response = client.post(reverse("delete_job", args=[job.id]))

    assert response.status_code == 302
    assert not Job.objects.filter(id=job.id).exists()
