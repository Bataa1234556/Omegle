from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Landing page with Connect button
    path('<str:room_name>/', views.room, name='room'),  # Chat room URL
]
