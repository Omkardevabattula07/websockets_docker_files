# chat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Room

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('rooms')
    return render(request, 'login.html')

@login_required
def rooms_view(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})

@login_required
def room_view(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room_name': room_name,
        'username': request.user.username,
    })

def logout_view(request):
    auth_logout(request)
    return redirect('login')
