from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

    # Text-based fields should NOT use null=True
    role = models.CharField(max_length=50, blank=True)

    # For dates, numbers etc → null=True is allowed
    date_of_birth = models.DateField(blank=True, null=True)

    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.user.username
