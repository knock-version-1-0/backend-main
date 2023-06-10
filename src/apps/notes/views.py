# notes/views.py
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets


class NoteListViewSet(viewsets.ViewSet):
    controller = None
    
    def create(self, request: Request) -> Response:
        return self.controller.create(
            request=request
        )
    
    def list(self, request: Request) -> Response:
        return self.controller.list(
            request=request
        )


class NoteDetailViewSet(viewsets.ViewSet):
    controller = None
    lookup_field = 'display_id'

    def retrieve(self, request: Request, display_id: str) -> Response:
        return self.controller.retrieve(
            request=request,
            key=display_id
        )
    
    def destroy(self, request: Request, display_id: str) -> Response:
        return self.controller.delete(
            request=request,
            key=display_id
        )
    
    def partial_update(self, request: Request, display_id: str) -> Response:
        return self.controller.update(
            request=request,
            key=display_id
        )
