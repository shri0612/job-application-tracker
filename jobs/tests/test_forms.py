from django.test import TestCase
from accounts.forms import CustomUserCreationForm

class FormTest(TestCase):
    def test_valid_form(self):
        form = CustomUserCreationForm(data={
            "email": "test@example.com",
            "password1": "Admin123@",
            "password2": "Admin123@"
        })
        self.assertTrue(form.is_valid())
