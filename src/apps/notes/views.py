# notes/views.py
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework import viewsets


class NoteListViewSet(viewsets.ViewSet):
    controller = None
    
    def create(self, request: HttpRequest) -> Response:
        return self.controller.create(
            request=request
        )


class NoteDetailViewset(viewsets.ViewSet):
    controller = None
    lookup_field = 'name'

    def retrieve(self, request: HttpRequest, name: str) -> Response:
        return self.controller.retrieve(
            request=request,
            key=name
        )
