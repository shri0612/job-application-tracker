from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.conf import settings

from .forms import CustomUserCreationForm, ProfileForm, EmailAuthenticationForm
from .models import Profile


# -------------------------
# REGISTER (GET + POST)
# -------------------------
@never_cache
@require_http_methods(["GET", "POST"])
def register(request):

    if request.user.is_authenticated:
        return redirect("job_list")

    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        # Fix help text safety
        if user_form.fields.get("password1").help_text:
            user_form.fields["password1"].help_text = mark_safe(
                user_form.fields["password1"].help_text
            )

        if user_form.is_valid() and profile_form.is_valid():

            # Create user
            user = user_form.save(commit=False)
            user.username = user.email.split("@")[0].lower()
            user.save()

            # Create profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.email = user.email
            profile.save()

            # Send welcome email
            subject = f"Welcome {user.username} 🎉 - Registration Successful"
            html_content = f"""
            <html><body>
                <h2 style="color:#0d6efd;">Hi {user.username},</h2>
                <p>Thank you for registering on <b>Job Application Tracker</b>!</p>
                <p>This is an automated email — do not reply.</p>
            </body></html>
            """
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            email.attach_alternative(html_content, "text/html")

            try:
                email.send()
            except Exception:
                pass

            return redirect(f"{reverse('login')}?registered=1")

    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

        if user_form.fields.get("password1").help_text:
            user_form.fields["password1"].help_text = mark_safe(
                user_form.fields["password1"].help_text
            )

    return render(request, "accounts/register.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })


# -------------------------
# LOGIN
# -------------------------
@never_cache
@require_http_methods(["GET", "POST"])
def login_view(request):

    if request.user.is_authenticated:
        return redirect("job_list")

    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("job_list")
    else:
        form = EmailAuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


# -------------------------
# LOGOUT (GET)
# -------------------------
@never_cache
@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------------
# PROFILE VIEW
# -------------------------
@login_required
@require_http_methods(["GET"])
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})
