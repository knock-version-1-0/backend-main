from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notes/(?P<note_id>\d+)/update-keyword/$', consumers.NoteUpdateKeyword.as_asgi()),
    re_path(r'ws/notes/(?P<note_id>\d+)/create-keyword/$', consumers.NoteCreateKeyword.as_asgi())
]
