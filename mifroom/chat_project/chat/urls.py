# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rooms/', views.rooms_view, name='rooms'),
    path('rooms/<str:room_name>/', views.room_view, name='room'),
]
