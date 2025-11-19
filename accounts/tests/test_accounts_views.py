from django.urls import reverse

def test_login_page_loads(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200

def test_register_page_loads(client):
    response = client.get(reverse("register"))
    assert response.status_code == 200