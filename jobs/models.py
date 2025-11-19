from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
        ('Wishlist', 'Wishlist'),
    ]

    # ForeignKey: null=True is VALID (because no user = NULL in DB)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # CharField: DO NOT use null=True
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Applied')

    # DateField: null=True is correct (date may not exist)
    date_applied = models.DateField(null=True, blank=True)

    # TextField: remove null=True → blank=True is enough
    notes = models.TextField(blank=True)

    # Use Django built-ins instead of overriding save()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
