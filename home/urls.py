from django.urls import path
from . import views


urlpatterns = [



    path('', views.home, name='home'),



    path('ai-chat/', views.ai_chat, name='ai_chat'),  
]