from .models import Booking, Notification, ChatRoom
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from influencers.models import InfluencerProfile
from .models import Booking, Notification, ChatRoom


@login_required
def dashboard(request):
    profile = InfluencerProfile.objects.get(user=request.user)

    bookings = Booking.objects.filter(
        influencer=profile
    ).order_by('-created_at')[:4]

    total_requests = Booking.objects.filter(influencer=profile).count()
    accepted_requests = Booking.objects.filter(
        influencer=profile, status='approved'
    ).count()

    total_earnings = Booking.objects.filter(
        influencer=profile, status='approved'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'influencers/dashboard.html', {
        'bookings': bookings,
        'total_requests': total_requests,
        'accepted_requests': accepted_requests,
        'total_earnings': total_earnings,
        'profile': profile
    })

@login_required
def create_booking(request, influencer_id):
    influencer = get_object_or_404(InfluencerProfile, id=influencer_id)

    if request.method == 'POST':
        booking = Booking.objects.create(
            influencer=influencer,
            shopkeeper=request.user,
            business_name=request.POST.get('business_name'),
            message=request.POST.get('message'),
            category=influencer.category or 'General',
            location=influencer.location or '',
            amount=request.POST.get('amount') or 0,
            booking_date=request.POST.get('date'),
            booking_time=request.POST.get('time')
        )

        
        Notification.objects.create(
            recipient=booking.influencer.user,
            sender=request.user,
            notif_type='booking_request',
            booking=booking,
            message=f"{request.user.username} ne booking request bheji"
        )

        messages.success(request, "Booking request sent!")
        return redirect('influencers:influencer_detail', id=influencer.id)

    return render(request, 'bookings/create_booking.html', {'influencer': influencer})


@login_required
def send_booking_request(request, influencer_id):
    influencer = get_object_or_404(InfluencerProfile, id=influencer_id)

    if request.method == 'POST':
        booking = Booking.objects.create(
            influencer=influencer,
            shopkeeper=request.user,
            business_name=request.POST.get('business_name'),
            message=request.POST.get('message'),
            category=influencer.category or 'General',
            location=influencer.location or '',
            amount=request.POST.get('amount') or 0,
            booking_date=request.POST.get('date'),
            booking_time=request.POST.get('time'),
            status='pending'
        )

        Notification.objects.create(
            recipient=booking.influencer.user,
            sender=request.user,
            notif_type='booking_request',
            booking=booking,
            message=f"{request.user.username} ne booking request bheji"
        )

        return JsonResponse({'status': 'ok'})



@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.influencer.user != request.user:
        return redirect('bookings:dashboard')

    booking.status = 'approved'
    booking.save()

    
    Notification.objects.create(
        recipient=booking.shopkeeper,
        sender=request.user,
        notif_type='booking_approved',
        booking=booking,
        message=f"{request.user.username} ne aapki booking accept kar li!"
    )

    
    ChatRoom.objects.get_or_create(booking=booking)

    messages.success(request, "Booking accepted!")
    return redirect('bookings:dashboard')



@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.influencer.user != request.user:
        return redirect('bookings:dashboard')

    booking.status = 'rejected'
    booking.save()

    Notification.objects.create(
        recipient=booking.shopkeeper,
        sender=request.user,
        notif_type='booking_rejected',
        booking=booking,
        message=f"{request.user.username} ne aapki booking reject kar di"
    )

    messages.error(request, "Booking rejected.")
    return redirect('bookings:dashboard')


@login_required
def respond_to_booking(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.influencer.user != request.user:
        return JsonResponse({'status': 'error'})

    if action == 'accept':
        booking.status = 'approved'
        notif_type = 'booking_approved'
        msg = "Booking accept ho gayi! Chat start karo."

        ChatRoom.objects.get_or_create(booking=booking)

    else:
        booking.status = 'rejected'
        notif_type = 'booking_rejected'
        msg = "Booking reject ho gayi."

    booking.save()

    Notification.objects.create(
        recipient=booking.shopkeeper,
        sender=request.user,
        notif_type=notif_type,
        booking=booking,
        message=msg
    )

    return JsonResponse({'status': 'ok'})


@login_required
def all_bookings(request):
    profile = InfluencerProfile.objects.get(user=request.user)
    status_filter = request.GET.get('status')

    bookings = Booking.objects.filter(influencer=profile)

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    bookings = bookings.order_by('-created_at')

    return render(request, 'bookings/all_bookings.html', {
        'bookings': bookings,
        'current_filter': status_filter
    })


@login_required
def analytics(request):
    profile = InfluencerProfile.objects.get(user=request.user)

    total = Booking.objects.filter(influencer=profile).count()
    approved = Booking.objects.filter(influencer=profile, status='approved').count()
    rejected = Booking.objects.filter(influencer=profile, status='rejected').count()

    earnings = Booking.objects.filter(
        influencer=profile,
        status='approved'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'bookings/analytics.html', {
        'profile': profile,
        'total_bookings': total,
        'approved_bookings': approved,
        'rejected_bookings': rejected,
        'total_earnings': earnings
    })


@login_required
def get_notifications(request):
    notifs = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).select_related('sender', 'booking')[:20]

    data = [{
        'id': n.id,
        'type': n.notif_type,
        'message': n.message,
        'booking_id': n.booking.id if n.booking else None,
        'sender': n.sender.username,
        'created_at': n.created_at.strftime('%d %b, %I:%M %p'),
    } for n in notifs]

    return JsonResponse({'notifications': data, 'count': len(data)})


@login_required
def mark_read(request, notif_id):
    Notification.objects.filter(
        id=notif_id,
        recipient=request.user
    ).update(is_read=True)

    return JsonResponse({'status': 'ok'})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    return render(request, 'bookings/notifications.html', {
        'notifications': notifications
    })

@login_required
def chat_room(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    room, created = ChatRoom.objects.get_or_create(booking=booking)

    return render(request, 'bookings/chat.html', {
        'room': room,
        'booking': booking
    })


@login_required
def api_my_bookings(request):
    """
    FAB chat bubble ke liye bookings list.
    ChatRoom model use karta hai (ChatMessage nahi).
    """
    is_influencer = hasattr(request.user, 'influencerprofile')

    if is_influencer:
        
        try:
            profile = request.user.influencerprofile
            bookings = Booking.objects.filter(
                influencer=profile
            ).select_related('shopkeeper').order_by('-created_at')[:20]

            data = []
            for b in bookings:
                data.append({
                    'id': b.id,
                    'name': b.business_name or b.shopkeeper.username,
                    'status': b.status,
                    'unread': False,  
                })
        except Exception:
            data = []
    else:
        
        bookings = Booking.objects.filter(
            shopkeeper=request.user
        ).select_related('influencer__user').order_by('-created_at')[:20]

        data = []
        for b in bookings:
            data.append({
                'id': b.id,
                'name': b.influencer.user.username,
                'status': b.status,
                'unread': False,
            })

    return JsonResponse({'bookings': data})


@login_required
def api_chat_messages(request, booking_id):
    """
    FAB chat bubble ke liye messages.
    ChatRoom ke through messages fetch karta hai.
    """
    try:
        booking = get_object_or_404(Booking, id=booking_id)

        
        is_shopkeeper = (booking.shopkeeper == request.user)
        is_influencer = (
            hasattr(request.user, 'influencerprofile') and
            booking.influencer == request.user.influencerprofile
        )

        if not (is_shopkeeper or is_influencer):
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        
        try:
            room = ChatRoom.objects.get(booking=booking)
        
            msgs = room.messages.select_related('sender').order_by('created_at')[:50]

            data = [{
                'sender': m.sender.username,
                'message': m.content,  
                'created_at': m.created_at.strftime('%H:%M') if m.created_at else '',
            } for m in msgs]

        except ChatRoom.DoesNotExist:
            data = []

        return JsonResponse({
            'messages': data,
            'current_user': request.user.username,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)