from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from influencers.models import InfluencerProfile
from .models import Booking


@login_required
def dashboard(request):
    profile, created = InfluencerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'bio': '',
            'followers': 0,
            'category': 'General',
            'location': 'India',
            'price_per_post': 0
        }
    )

    bookings = Booking.objects.filter(
        influencer=profile
    ).order_by('-created_at')[:4]

    total_requests = Booking.objects.filter(
        influencer=profile
    ).count()

    accepted_requests = Booking.objects.filter(
        influencer=profile,
        status='approved'
    ).count()

    total_earnings = Booking.objects.filter(
        influencer=profile,
        status='approved'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'bookings': bookings,
        'total_requests': total_requests,
        'accepted_requests': accepted_requests,
        'total_earnings': total_earnings,
        'profile': profile
    }

    return render(request, 'influencers/dashboard.html', context)


@login_required
def approve_booking(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)

        if booking.influencer.user != request.user:
            return redirect('bookings:dashboard')

        booking.status = 'approved'
        booking.save()

        messages.success(request, "Booking accepted successfully!")

    return redirect('bookings:dashboard')


@login_required
def reject_booking(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)

        if booking.influencer.user != request.user:
            return redirect('bookings:dashboard')

        booking.status = 'rejected'
        booking.save()

        messages.error(request, "Booking rejected.")

    return redirect('bookings:dashboard')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_booking(request, influencer_id):
    influencer = get_object_or_404(InfluencerProfile, id=influencer_id)

    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        message = request.POST.get('message')
        # ✅ FIXED: category aur location influencer profile se lo
        # Form mein yeh fields nahi hain isliye POST se None aata tha
        category = influencer.category or 'General'
        location = influencer.location or ''
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        time = request.POST.get('time')

        Booking.objects.create(
            influencer=influencer,
            shopkeeper=request.user,
            business_name=business_name,
            message=message,
            category=category,
            location=location,
            amount=amount if amount else 0,
            booking_date=date,
            booking_time=time
        )

        messages.success(request, "Booking request sent!")

        return redirect('shopkeepers:my_bookings')

    return render(request, 'bookings/create_booking.html', {
        'influencer': influencer
    })


@login_required
def all_bookings(request):
    profile = InfluencerProfile.objects.get(user=request.user)
    status_filter = request.GET.get('status')

    bookings = Booking.objects.filter(influencer=profile)

    if status_filter == 'pending':
        bookings = bookings.filter(status='pending')
    elif status_filter == 'approved':
        bookings = bookings.filter(status='approved')
    elif status_filter == 'rejected':
        bookings = bookings.filter(status='rejected')

    bookings = bookings.order_by('-created_at')

    return render(request, 'bookings/all_bookings.html', {
        'bookings': bookings,
        'current_filter': status_filter
    })


@login_required
def analytics(request):
    profile = InfluencerProfile.objects.get(user=request.user)

    total_bookings = Booking.objects.filter(influencer=profile).count()
    approved_bookings = Booking.objects.filter(influencer=profile, status='approved').count()
    rejected_bookings = Booking.objects.filter(influencer=profile, status='rejected').count()

    total_earnings = Booking.objects.filter(
        influencer=profile,
        status='approved'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'profile': profile,
        'total_bookings': total_bookings,
        'approved_bookings': approved_bookings,
        'rejected_bookings': rejected_bookings,
        'total_earnings': total_earnings
    }

    return render(request, 'bookings/analytics.html', context)