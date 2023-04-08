from rest_framework.request import HttpRequest
from rest_framework.response import Response
from core.controller import BaseController

from adapters.services.notes_service import (
    NoteService,
)
from adapters.dto.notes_dto import (
    NoteDto,
)

__all__ = [
    'NoteController',
]


class NoteController(BaseController):
    
    def __init__(self, service: NoteService):
        self.service = service
    
    def retrieve(self, request: HttpRequest, key: str) -> Response:
        name = key
        payload, status = self.service.retrieve(key=name, user_id=request.user.pk)
        if isinstance(payload, NoteDto):
            return Response(payload.dict(), status=status)
        return Response(payload, status=status)
    
    def create(self, request: HttpRequest) -> Response:
        payload, status = self.service.create(request.data, user_id=request.user.pk)
        return Response(payload, status=status)
