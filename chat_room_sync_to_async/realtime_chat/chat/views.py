# chat/views.py

from django.shortcuts import render, redirect
from .models import Room, Message

def index(request):
    # Display all existing rooms
    rooms = Room.objects.all()
    return render(request, 'index.html', {'rooms': rooms})

def create_room(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        if room_name:
            room, created = Room.objects.get_or_create(name=room_name)
            if created:
                return redirect('room', room_name=room.name)
    return redirect('index')

def room(request, room_name):
    # Display messages for a specific room
    room = Room.objects.get(name=room_name)
    messages = room.messages.order_by('timestamp')  # Get all messages in this room
    return render(request, 'room.html', {
        'room': room,
        'messages': messages,
    })
