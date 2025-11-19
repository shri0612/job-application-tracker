from django.urls import reverse
from django.test import Client

def test_smoke():
    """
    Basic smoke test to ensure the application loads a main page.
    """
    client = Client()
    response = client.get(reverse("job_list"))  # your main page
    assert response.status_code == 200
