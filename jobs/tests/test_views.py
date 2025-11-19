from django.urls import reverse

def test_jobs_redirect_without_login(client):
    response = client.get(reverse("job_list"))
    assert response.status_code in (302, 301)
