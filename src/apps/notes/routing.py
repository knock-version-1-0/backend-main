from django.urls import re_path

from . import consumers
from di.notes_factory import KeywordFactory


websocket_urlpatterns = [
    re_path(r'ws/notes/(?P<note_id>\d+)/keyword/$', consumers.NoteKeywordConsumer.as_asgi(factory=KeywordFactory())),
]
