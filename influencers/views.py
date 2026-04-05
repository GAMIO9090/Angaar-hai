from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from .forms import InfluencerProfileForm
from .models import InfluencerProfile
from bookings.models import Booking


@login_required
def influencer_dashboard(request):
    profile, created = InfluencerProfile.objects.get_or_create(user=request.user)
    
    total_bookings = Booking.objects.filter(influencer=profile).count()
    accepted_bookings = Booking.objects.filter(influencer=profile, status='approved').count()
    total_earnings = Booking.objects.filter(influencer=profile, status='approved').aggregate(
        total=models.Sum('amount'))['total'] or 0
    recent_bookings = Booking.objects.filter(influencer=profile).order_by('-created_at')[:5]

    return render(request, 'influencers/dashboard.html', {
        'profile': profile,
        'total_bookings': total_bookings,
        'accepted_bookings': accepted_bookings,
        'total_earnings': total_earnings,
        'recent_bookings': recent_bookings,
    })


@login_required
def edit_profile(request):
    profile, created = InfluencerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = InfluencerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('influencers:dashboard')
    else:
        form = InfluencerProfileForm(instance=profile)

    return render(request, 'influencers/edit_profile.html', {'form': form})


def influencers_list(request):
    influencers = InfluencerProfile.objects.all()
    return render(request, 'influencers/influencers.html', {'influencers': influencers})


def influencer_detail(request, id):
    influencer = get_object_or_404(InfluencerProfile, id=id)
    return render(request, 'influencers/detail.html', {'influencer': influencer})