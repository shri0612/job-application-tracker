import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_job_list_page_loads(client):
    response = client.get(reverse("job_list"))
    assert response.status_code == 200
