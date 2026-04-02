from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),

    path('logout/', views.logout_view, name='logout'),

    
    path('create/<int:influencer_id>/', views.create_booking, name='create_booking'),

    path('all/', views.all_bookings, name='all_bookings'),
    path('analytics/', views.analytics, name='analytics'),
]