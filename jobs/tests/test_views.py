import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from jobs.models import Job


# -------------------------------
# 1. job_list view
# -------------------------------
@pytest.mark.django_db
def test_job_list_page_loads(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    Job.objects.create(
        title="Test Job",
        company="Test Company",
        status="Applied",
        notes="Testing notes",
        user=user
    )

    response = client.get(reverse("job_list"))
    
    assert response.status_code == 200
    assert b"Test Job" in response.content


# -------------------------------
# 2. add_job view
# -------------------------------
@pytest.mark.django_db
def test_add_job_creates_entry(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    job_data = {
        "title": "Backend Developer",
        "company": "Google",
        "status": "Applied",
        "notes": "A test note",
        "date_applied": "2025-01-01"
    }

    response = client.post(reverse("add_job"), job_data)

    assert response.status_code == 302
    assert Job.objects.filter(title="Backend Developer", user=user).exists()


# -------------------------------
# 3. edit_job view
# -------------------------------
@pytest.mark.django_db
def test_edit_job_updates_entry(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    job = Job.objects.create(
        title="Old Title",
        company="Test Company",
        status="Applied",
        notes="Old note",
        user=user
    )

    updated_data = {
        "title": "New Title",
        "company": "Test Company",
        "status": "Interview",
        "notes": "Updated note"
    }

    response = client.post(reverse("edit_job", args=[job.id]), updated_data)

    assert response.status_code == 302

    job.refresh_from_db()
    assert job.title == "New Title"
    assert job.status == "Interview"
    assert job.notes == "Updated note"


# -------------------------------
# 4. delete_job view
# -------------------------------
@pytest.mark.django_db
def test_delete_job_removes_entry(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    job = Job.objects.create(
        title="Delete Me",
        company="Test Company",
        status="Applied",
        notes="Delete note",
        user=user
    )

    response = client.post(reverse("delete_job", args=[job.id]))

    assert response.status_code == 302
    assert not Job.objects.filter(id=job.id).exists()
