from django.shortcuts import render
from django.http import HttpResponse
import random
import string
import uuid

def home(request):
    random_room_name = uuid.uuid4().hex  # Generate a unique room name
    return render(request, 'home.html', {'random_room_name': random_room_name})

def room(request, room_name):
    """Room page where the user is connected to a specific chat room"""
    return render(request, 'room.html', {
        'room_name': room_name
    })
