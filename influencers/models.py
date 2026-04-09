from django.db import models
from django.conf import settings


class InfluencerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    phone = models.CharField(max_length=20, blank=True, default='')
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='influencer_photos/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='influencer_profiles/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='influencer_banners/', null=True, blank=True)

    street = models.CharField(max_length=200, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    pincode = models.CharField(max_length=10, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='India')

    bio = models.TextField(blank=True, default='')
    category = models.CharField(max_length=100, blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    price_per_post = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)

    instagram = models.URLField(blank=True, default='')
    youtube = models.URLField(blank=True, default='')
    twitter = models.URLField(blank=True, default='')

    def __str__(self):
        return self.user.username


from django.contrib import admin
admin.site.register(InfluencerProfile)