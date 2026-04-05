from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('influencer', 'Influencer'),
        ('shopkeeper', 'Shopkeeper'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='')