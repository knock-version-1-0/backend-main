# chat/urls.py
from core.routers import Router

from django.urls import path, include
from . import views

from di.notes_factory import NoteFactory


router = Router()

router.register(
    '', views.NoteViewSet, basename='note', factory=NoteFactory()
)


urlpatterns = [
    path('', include(router.urls))
]
