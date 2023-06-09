import json

from rest_framework.request import Request
from rest_framework.response import Response
from dataclasses import asdict
from core.controller import HttpController, WsController

from adapters.services.notes_service import (
    NoteService,
    KeywordService
)


class NoteController(HttpController):
    
    def __init__(self, service: NoteService):
        self.service = service
    
    def list(self, request: Request) -> Response:
        payload, status = self.service.list(params=request.query_params, user_id=request.user.pk)

        return Response(asdict(payload), status=status)
    
    def retrieve(self, request: Request, key: str) -> Response:
        display_id = key
        payload, status = self.service.retrieve(key=display_id, user_id=request.user.pk)
        
        return Response(asdict(payload), status=status)
    
    def create(self, request: Request) -> Response:
        payload, status = self.service.create(request.data, user_id=request.user.pk)
        
        return Response(asdict(payload), status=status)
    
    def update(self, request: Request, key: str) -> Response:
        display_id = key
        payload, status = self.service.update(key=display_id, data=request.data, user_id=request.user.pk)

        return Response(asdict(payload), status=status)
    
    def delete(self, request: Request, key: str) -> Response:
        display_id = key
        payload, status = self.service.delete(key=display_id, user_id=request.user.pk)

        return Response(asdict(payload), status=status)


class KeywordController(WsController):

    def __init__(self, service: KeywordService):
        self.service = service
    
    def create(self, event) -> str:
        data = self._parse(event)
        payload, _ = self.service.create(data)

        return json.dumps(asdict(payload))
