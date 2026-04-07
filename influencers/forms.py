from django import forms
from .models import InfluencerProfile
from bookings.models import Booking


class InfluencerProfileForm(forms.ModelForm):
    class Meta:
        model = InfluencerProfile
        fields = [
            'phone', 'date_of_birth', 'photo',
            'street', 'city', 'state', 'pincode', 'country',
            'bio', 'category', 'location', 'price_per_post',
            'instagram', 'youtube', 'twitter',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write something about yourself'
            }),
            'category': forms.TextInput(attrs={
                'placeholder': 'Your niche/category'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Your city/country'
            }),
            'price_per_post': forms.NumberInput(attrs={
                'placeholder': 'Price per post in ₹'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+91 98765 43210'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date'
            }),
            'street': forms.TextInput(attrs={
                'placeholder': 'e.g. Sector 12, Rohini'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'New Delhi'
            }),
            'pincode': forms.TextInput(attrs={
                'placeholder': '110001',
                'maxlength': '6'
            }),
            'country': forms.TextInput(attrs={
                'placeholder': 'India'
            }),
            'instagram': forms.URLInput(attrs={
                'placeholder': 'https://instagram.com/yourhandle'
            }),
            'youtube': forms.URLInput(attrs={
                'placeholder': 'https://youtube.com/yourchannel'
            }),
            'twitter': forms.URLInput(attrs={
                'placeholder': 'https://twitter.com/yourhandle'
            }),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['influencer']
        widgets = {
            'influencer': forms.Select(attrs={'disabled': True})
        }