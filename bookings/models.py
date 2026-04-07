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



class Notification(models.Model):
    NOTIF_TYPES = [
        ('booking_request', 'Booking Request'),
        ('booking_approved', 'Booking Approved'),
        ('booking_rejected', 'Booking Rejected'),
        ('new_message', 'New Message'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )

    notif_type = models.CharField(max_length=30, choices=NOTIF_TYPES)

    message = models.TextField(blank=True)

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notif_type} → {self.recipient.username}"



class ChatRoom(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='chatroom'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat: {self.booking.business_name} <-> {self.booking.influencer.user.username}"


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:40]}"