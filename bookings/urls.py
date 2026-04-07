from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    
    path('', views.dashboard, name='dashboard'),

    
    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),


    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),


    
    path('create/<int:influencer_id>/', views.create_booking, name='create_booking'),

   
    path('all/', views.all_bookings, name='all_bookings'),

   
    path('analytics/', views.analytics, name='analytics'),

    
    path('notifications/', views.get_notifications, name='get_notifications'),

    path('notifications/read/<int:notif_id>/', views.mark_read, name='mark_read'),

    path('notifications-page/', views.notifications_page, name='notifications_page'),

    path('chat/<int:booking_id>/', views.chat_room, name='chat_room'),

    
    path('logout/', views.logout_view, name='logout'),
]