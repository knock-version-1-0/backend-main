from rest_framework.request import HttpRequest
from rest_framework.response import Response
from core.controller import BaseController

from adapters.services.notes_service import (
    NoteService,
)

__all__ = [
    'NoteController',
]


class NoteController(BaseController):
    
    def __init__(self, service: NoteService):
        self.service = service
    
    def list(self, request: HttpRequest) -> Response:
        payload, status = self.service.list(params=request.query_params, user_id=request.user.pk)

        return Response(payload, status=status)
    
    def retrieve(self, request: HttpRequest, key: str) -> Response:
        display_id = key
        payload, status = self.service.retrieve(key=display_id, user_id=request.user.pk)
        
        return Response(payload, status=status)
    
    def create(self, request: HttpRequest) -> Response:
        payload, status = self.service.create(request.data, user_id=request.user.pk)
        
        return Response(payload, status=status)
