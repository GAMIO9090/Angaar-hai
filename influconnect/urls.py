from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),


    path('', include('home.urls')),
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),

    path('influencers/', include('influencers.urls', namespace='influencers')),

    
    path('shopkeepers/', include(('shopkeepers.urls', 'shopkeepers'), namespace='shopkeepers')
         
         ),

    path('bookings/', include('bookings.urls')),
    path('accounts/', include('django.contrib.auth.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)