from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import secrets, string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import CustomUserCreationForm, ProfileForm, EmailAuthenticationForm
from .models import Profile


# 🧾 Generate random username
def _generate_username(length=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


@never_cache
def register(request):
    """Handles new user registration (no profile picture, Gmail SMTP)."""

    if request.user.is_authenticated:
        return redirect("job_list")

    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            # -------------------------
            # Create User
            # -------------------------
            user = user_form.save(commit=False)
            user.username = user.email.split("@")[0].lower()
            user.save()

            # -------------------------
            # Create Profile
            # -------------------------
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.email = user.email
            profile.save()

            # -------------------------
            # Send Welcome Email (Gmail SMTP)
            # -------------------------
            subject = f"Welcome {user.username} 🎉 - Registration Successful"

            html_content = f"""
            <html>
            <body style="font-family: Arial; line-height:1.6;">
                <h2 style="color:#0d6efd;">Hi {user.username},</h2>
                <p>Thank you for registering on <b>Job Application Tracker</b>!</p>
                <p>You can now log in and start tracking your job applications easily.</p>
                <p style="color:gray; font-size:12px;">This is an automated email — please do not reply.</p>
            </body>
            </html>
            """

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,   # Gmail sender from settings.py
                [user.email],
            )
            email.attach_alternative(html_content, "text/html")

            try:
                email.send()
            except Exception as e:
                print("⚠️ Error sending registration email:", e)

            return redirect(f"{reverse('login')}?registered=1")

    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    return render(request, "accounts/register.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })



@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect("job_list")

    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("job_list")
    else:
        form = EmailAuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


@never_cache
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request):
    """Display logged-in user's profile info and picture"""
    profile = request.user.profile  # get profile linked to user
    return render(request, "accounts/profile.html", {"profile": profile})