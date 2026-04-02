from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from influencers.models import InfluencerProfile
from bookings.models import Booking
from .forms import ShopkeeperProfileForm


@login_required
def shopkeeper_dashboard(request):
    bookings = Booking.objects.filter(
        shopkeeper=request.user
    ).order_by('-created_at')[:5]

    total_bookings = Booking.objects.filter(
        shopkeeper=request.user
    ).count()

    influencers = InfluencerProfile.objects.all()

    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'recommended_influencers': influencers  
    }

    return render(request, 'shopkeepers/dashboard.html', context)


@login_required
def browse_influencers(request):
    influencers = InfluencerProfile.objects.all()

    return render(request, 'shopkeepers/browse_influencers.html', {
        'influencers': influencers
    })


@login_required
def shopkeeper_profile(request):
    if request.method == 'POST':
        form = ShopkeeperProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('shopkeepers:shopkeeper_dashboard')
    else:
        form = ShopkeeperProfileForm(instance=request.user)

    return render(request, 'shopkeepers/edit_profile.html', {
        'form': form
    })


@login_required
def view_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        shopkeeper=request.user
    )

    return render(request, 'shopkeepers/booking_detail.html', {
        'booking': booking
    })


@login_required
def create_booking(request, influencer_id):
    influencer = get_object_or_404(
        InfluencerProfile,
        id=influencer_id
    )

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')

        Booking.objects.create(
            influencer=influencer,
            shopkeeper=request.user,
            date=date,
            time=time
        )

        messages.success(
            request,
            f"Booking created for {influencer.user.username}"
        )

        return redirect('shopkeepers:my_bookings') 

    return render(request, 'bookings/create_booking.html', {
        'influencer': influencer
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        shopkeeper=request.user
    ).order_by('-created_at')

   
    return render(request, 'bookings/all_bookings.html', {
        'bookings': bookings
    })


@login_required
def analytics(request):
    bookings = Booking.objects.filter(shopkeeper=request.user)

    total = bookings.count()

    return render(request, 'shopkeepers/analytics.html', {
        'total_bookings': total
    })