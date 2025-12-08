import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from accounts.models import Profile



# REGISTER VIEW TESTS

@pytest.mark.django_db
def test_register_page_loads(client):
    response = client.get(reverse("register"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_creates_user_and_profile(client):
    data = {
        "email": "test@example.com",
        "password1": "Testpass123!",
        "password2": "Testpass123!",
        "date_of_birth": "2000-01-01",
        "phone_number": "1234567890",
        "address": "Test Street",
        "city": "Dublin",
        "postal_code": "A001",
    }

    response = client.post(reverse("register"), data)
    
    # Should redirect to login with ?registered=1
    assert response.status_code == 302
    assert "login" in response.url

    # User should exist
    user = User.objects.filter(email="test@example.com").first()
    assert user is not None

    # Profile should exist
    profile = Profile.objects.filter(user=user).first()
    assert profile is not None



# LOGIN VIEW TESTS

@pytest.mark.django_db
def test_login_page_loads(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_valid_user(client):
    User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="Testpass123!"
    )

    response = client.post(
        reverse("login"),
        {"username": "test@example.com", "password": "Testpass123!"}
    )

    assert response.status_code == 302
    assert response.url == reverse("job_list")

    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="Testpass123!"
    )

    response = client.post(
        reverse("login"),
        {"email": "test@example.com", "password": "Testpass123!"}
    )

    assert response.status_code == 302  # redirect to job_list
    assert response.url == reverse("job_list")

    # must be logged in
    user = get_user(client)
    assert user.is_authenticated



# LOGOUT VIEW TEST

@pytest.mark.django_db
def test_logout_logs_out_user(client):
    user = User.objects.create_user(username="testuser", password="pass12345")
    client.login(username="testuser", password="pass12345")

    response = client.get(reverse("logout"))
    assert response.status_code == 302
    assert response.url == reverse("login")

    # should be logged out
    user = get_user(client)
    assert not user.is_authenticated



# PROFILE VIEW TESTS

@pytest.mark.django_db
def test_profile_requires_login(client):
    response = client.get(reverse("profile"))
    assert response.status_code == 302
    assert "/login/" in response.url


@pytest.mark.django_db
def test_profile_loads_for_authenticated_user(client):
    user = User.objects.create_user(username="testuser", password="pass12345", email="a@a.com")
    Profile.objects.create(user=user, email=user.email)

    client.login(username="testuser", password="pass12345")
    response = client.get(reverse("profile"))

    assert response.status_code == 200
    assert b"profile" or b"email" in response.content
