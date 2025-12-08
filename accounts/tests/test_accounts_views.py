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
    assert response.status_code == 302
    assert "login" in response.url

    user = User.objects.filter(email="test@example.com").first()
    assert user is not None

    profile = Profile.objects.filter(user=user).first()
    assert profile is not None



# LOGIN VIEW TESTS


@pytest.mark.django_db
def test_login_page_loads(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_valid_user(client):
    # 🔥 IMPORTANT: username = email because the login form uses email as username
    User.objects.create_user(
        username="test@example.com",
        email="test@example.com",
        password="Testpass123!"
    )

    # Login form expects: {"username": email, "password": password}
    response = client.post(
        reverse("login"),
        {"username": "test@example.com", "password": "Testpass123!"}
    )

    assert response.status_code == 302
    assert response.url == reverse("job_list")

    logged_in_user = get_user(client)
    assert logged_in_user.is_authenticated



# LOGOUT VIEW TEST


@pytest.mark.django_db
def test_logout_logs_out_user(client):
    user = User.objects.create_user(
        username="logout@example.com",
        email="logout@example.com",
        password="pass12345"
    )

    client.login(username="logout@example.com", password="pass12345")

    response = client.get(reverse("logout"))
    assert response.status_code == 302
    assert response.url == reverse("login")

    logged_in_user = get_user(client)
    assert not logged_in_user.is_authenticated



# PROFILE VIEW TESTS


@pytest.mark.django_db
def test_profile_requires_login(client):
    response = client.get(reverse("profile"))
    assert response.status_code == 302
    assert "/login/" in response.url


@pytest.mark.django_db
def test_profile_loads_for_authenticated_user(client):
    user = User.objects.create_user(
        username="a@a.com",
        email="a@a.com",
        password="pass12345"
    )

    Profile.objects.create(user=user, email=user.email)

    client.login(username="a@a.com", password="pass12345")
    response = client.get(reverse("profile"))

    assert response.status_code == 200

    # The profile page should display the user's email somewhere
    assert user.email.encode() in response.content
