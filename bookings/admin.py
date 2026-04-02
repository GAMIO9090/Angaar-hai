
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('shopkeeper', 'influencer', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('shopkeeper__username', 'influencer__user__username')