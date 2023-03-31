# note/views.py
from django.shortcuts import render


def index(request):
    return render(request, "note/index.html")


def room(request, room_name):
    return render(request, "note/room.html", {"room_name": room_name})
