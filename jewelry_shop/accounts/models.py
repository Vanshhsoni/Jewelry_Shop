from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # username, password, email already included in AbstractUser
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
