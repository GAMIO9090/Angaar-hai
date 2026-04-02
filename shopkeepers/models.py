from django.db import models
from django.conf import settings

class ShopkeeperProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.shop_name
    
from django.contrib import admin
from .models import ShopkeeperProfile

admin.site.register(ShopkeeperProfile)