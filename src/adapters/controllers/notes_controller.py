from rest_framework.request import Request as HttpRequest
from core.ws.request import Request as WsRequest
from rest_framework.response import Response as HttpResponse
from core.ws.response import Response as WsResponse
from dataclasses import asdict
from core.controller import HttpController, WsController

from adapters.services.notes_service import (
    NoteService,
    KeywordService
)


class NoteController(HttpController):
    
    def __init__(self, service: NoteService):
        self.service = service
    
    def list(self, request: HttpRequest) -> HttpResponse:
        payload, status = self.service.list(params=request.query_params, user_id=request.user.pk)

        return HttpResponse(asdict(payload), status=status)
    
    def retrieve(self, request: HttpRequest, key: str) -> HttpResponse:
        display_id = key
        payload, status = self.service.retrieve(key=display_id, user_id=request.user.pk)
        
        return HttpResponse(asdict(payload), status=status)
    
    def create(self, request: HttpRequest) -> HttpResponse:
        payload, status = self.service.create(request.data, user_id=request.user.pk)
        
        return HttpResponse(asdict(payload), status=status)
    
    def update(self, request: HttpRequest, key: str) -> HttpResponse:
        display_id = key
        payload, status = self.service.update(key=display_id, data=request.data, user_id=request.user.pk)

        return HttpResponse(asdict(payload), status=status)
    
    def delete(self, request: HttpRequest, key: str) -> HttpResponse:
        display_id = key
        payload, status = self.service.delete(key=display_id, user_id=request.user.pk)

        return HttpResponse(asdict(payload), status=status)


class KeywordController(WsController):

    def __init__(self, service: KeywordService):
        self.service = service
    
    def create(self, request: WsRequest) -> WsResponse:
        payload, status = self.service.create(data=request.data)

        return WsResponse(asdict(payload), status=status)
