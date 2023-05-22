from core.routers import Router

from django.urls import path, include
from . import views

from di.notes_factory import NoteFactory

router = Router()

router.register(
    '', views.NoteListViewSet, basename='notes', factory=NoteFactory()
)

router.register(
    '', views.NoteDetailViewSet, basename='notes', factory=NoteFactory()
)


urlpatterns = [
    path('notes/', include(router.urls))
]
