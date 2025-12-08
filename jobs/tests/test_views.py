import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from jobs.models import Job

@pytest.mark.django_db
def test_job_list_page_loads(client):
    # Create & login user
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    # Create a job for this user
    Job.objects.create(
        title="Test Job",
        company="Test Company",
        location="Dublin",
        status="Applied",
        user=user
    )

    # Request job list page
    response = client.get(reverse("job_list"))

    # Verify page loads
    assert response.status_code == 200
    assert b"Test Job" in response.content
