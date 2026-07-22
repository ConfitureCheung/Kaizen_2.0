from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_provider = models.BooleanField(default=False)
    is_client_user = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="provider_profile")
    company_name = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.company_name

