from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

# ✅ Login Form (Email-based)
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "autofocus": True,
            "placeholder": "you@example.com",
            "class": "form-control"
        })
    )


# ✅ User Creation Form (for User model)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "you@example.com",
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        """Ensure email is unique and case-insensitive."""
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


# ✅ Profile Form (for extra details + picture)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'role', 'date_of_birth', 'phone_number',
            'address', 'city', 'postal_code', 'profile_picture'
        ]
