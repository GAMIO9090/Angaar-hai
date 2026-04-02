from django.db import models
from django.conf import settings


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    shopkeeper = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shop_bookings'
    )

    influencer = models.ForeignKey(
        'influencers.InfluencerProfile',
        on_delete=models.CASCADE,
        related_name='influencer_bookings'
    )

    business_name = models.CharField(max_length=200, default="")
    message = models.TextField(default="")
    category = models.CharField(max_length=100, default="")
    location = models.CharField(max_length=200, blank=True, null=True)
    
    amount = models.PositiveIntegerField(default=0)

    
    booking_date = models.DateField(null=True, blank=True)
    booking_time = models.TimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} -> {self.influencer.user.username} ({self.status})"