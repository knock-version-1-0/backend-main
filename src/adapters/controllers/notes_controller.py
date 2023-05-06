from rest_framework.request import HttpRequest
from rest_framework.response import Response
from dataclasses import asdict
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

        return Response(asdict(payload), status=status)
    
    def retrieve(self, request: HttpRequest, key: str) -> Response:
        display_id = key
        payload, status = self.service.retrieve(key=display_id, user_id=request.user.pk)
        
        return Response(asdict(payload), status=status)
    
    def create(self, request: HttpRequest) -> Response:
        payload, status = self.service.create(request.data, user_id=request.user.pk)
        
        return Response(asdict(payload), status=status)
    
    def update(self, request: HttpRequest, key: str) -> Response:
        display_id = key
        payload, status = self.service.update(key=display_id, req_body=request.data, user_id=request.user.pk)

        return Response(asdict(payload), status=status)
    
    def delete(self, request: HttpRequest, key: str) -> Response:
        display_id = key
        payload, status = self.service.delete(key=display_id, user_id=request.user.pk)

        return Response(asdict(payload), status=status)
