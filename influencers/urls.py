from django.urls import path
from . import views

app_name = 'influencers'

urlpatterns = [
    path('', views.influencers_list, name='influencers_list'),



    path('<int:id>/', views.influencer_detail, name='influencer_detail'),
    

    path('dashboard/', views.influencer_dashboard, name='dashboard'),
    




    path('edit-profile/', views.edit_profile, name='edit_profile'),
]