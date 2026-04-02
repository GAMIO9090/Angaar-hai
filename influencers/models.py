from django.db import models
from django.conf import settings




class InfluencerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(default="")
    followers = models.IntegerField(default=0)
    category = models.CharField(max_length=100, default="General")
    location = models.CharField(max_length=100, default="India")
    price_per_post = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
from django.contrib import admin
from .models import InfluencerProfile

admin.site.register(InfluencerProfile)