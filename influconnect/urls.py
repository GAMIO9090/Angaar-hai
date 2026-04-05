from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 

    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('influencers/', include('influencers.urls', namespace='influencers')),
    path('shopkeepers/', include(('shopkeepers.urls', 'shopkeepers'), namespace='shopkeepers')),
    path('', include('bookings.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]