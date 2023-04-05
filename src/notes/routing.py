from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/note/(?P<room_name>\w+)/$", consumers.NoteConsumer.as_asgi()),
]
