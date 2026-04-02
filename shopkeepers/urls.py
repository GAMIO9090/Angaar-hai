from django.urls import path
from . import views

app_name = 'shopkeepers'

urlpatterns = [
    path('dashboard/', views.shopkeeper_dashboard, name='shopkeeper_dashboard'),
    path('profile/', views.shopkeeper_profile, name='shopkeeper_profile'),
    path('browse/', views.browse_influencers, name='browse_influencers'),
    path('booking/<int:booking_id>/', views.view_booking, name='view_booking'),
    path('booking/create/<int:influencer_id>/', views.create_booking, name='create_booking'),

    path('bookings/', views.my_bookings, name='my_bookings'),
    path('analytics/', views.analytics, name='analytics'),
    path('booking/create/<int:influencer_id>/', views.create_booking, name='create_booking'),
]