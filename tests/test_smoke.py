from django.urls import reverse
from django.test import Client

def test_smoke():
    """
    Basic smoke test to ensure the login page loads successfully.
    """
    client = Client()
    response = client.get(reverse("login"))
    assert response.status_code == 200
