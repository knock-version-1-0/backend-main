# notes/views.py
from django.shortcuts import render


def index(request):
    return render(request, "notes/index.html")


def room(request, room_name):
    return render(request, "notes/room.html", {"room_name": room_name})
