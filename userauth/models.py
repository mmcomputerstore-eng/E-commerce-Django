from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, blank=True, null=True, default='')
    is_vendor = models.BooleanField(default=False, help_text="Designates whether this user has vendor privileges (selected by Admin).")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    @property
    def is_vendor_user(self):
        if self.is_vendor or self.is_superuser:
            return True
        if hasattr(self, 'vendor_set') and self.vendor_set.exists():
            return True
        return False
