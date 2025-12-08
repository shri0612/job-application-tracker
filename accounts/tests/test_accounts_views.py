import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from accounts.models import Profile


# =====================================================
# REGISTER VIEW TESTS
# =====================================================

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


# =====================================================
# LOGIN VIEW TESTS
# =====================================================

@pytest.mark.django_db
def test_login_page_loads(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_valid_user(client):
    # Create a unique user
    User.objects.create_user(
        username="loginuser",
        email="test@example.com",
        password="Testpass123!"
    )

    # EmailAuthenticationForm expects email + password
    response = client.post(
        reverse("login"),
        {"email": "test@example.com", "password": "Testpass123!"}
    )

    # Should redirect to job_list after login
    assert response.status_code == 302
    assert response.url == reverse("job_list")

    # User must be logged in
    logged_in_user = get_user(client)
    assert logged_in_user.is_authenticated


# =====================================================
# LOGOUT VIEW TEST
# =====================================================

@pytest.mark.django_db
def test_logout_logs_out_user(client):
    user = User.objects.create_user(username="logoutuser", password="pass12345")
    client.login(username="logoutuser", password="pass12345")

    response = client.get(reverse("logout"))
    assert response.status_code == 302
    assert response.url == reverse("login")

    # Should be logged out
    logged_in_user = get_user(client)
    assert not logged_in_user.is_authenticated


# =====================================================
# PROFILE VIEW TESTS
# =====================================================

@pytest.mark.django_db
def test_profile_requires_login(client):
    response = client.get(reverse("profile"))
    assert response.status_code == 302
    assert "/login/" in response.url


@pytest.mark.django_db
def test_profile_loads_for_authenticated_user(client):
    user = User.objects.create_user(
        username="profileuser",
        password="pass12345",
        email="a@a.com"
    )

    Profile.objects.create(user=user, email=user.email)

    client.login(username="profileuser", password="pass12345")
    response = client.get(reverse("profile"))

    assert response.status_code == 200
    assert b"email" in response.content or b"profile" in response.content
