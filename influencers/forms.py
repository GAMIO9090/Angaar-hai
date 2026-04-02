from django import forms
from .models import InfluencerProfile
from bookings.models import Booking  

class InfluencerProfileForm(forms.ModelForm):
    class Meta:
        model = InfluencerProfile
        fields = ['bio', 'category', 'location', 'price_per_post']
        widgets = {
            'bio': forms.Textarea(attrs={'rows':3, 'placeholder':'Write something about yourself'}),
            'category': forms.TextInput(attrs={'placeholder':'Your niche/category'}),
            'location': forms.TextInput(attrs={'placeholder':'Your city/country'}),
            'price_per_post': forms.NumberInput(attrs={'placeholder':'Price per post in ₹'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['influencer']  
        widgets = {
            'influencer': forms.Select(attrs={'disabled': True})  
        }