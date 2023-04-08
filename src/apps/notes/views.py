# notes/views.py
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework import viewsets


class NoteViewSet(viewsets.ViewSet):
    controller = None

    def get(self, request: HttpRequest, name: str) -> Response:
        return self.controller.retrieve(
            request=request,
            key=name
        )
    
    def post(self, request: HttpRequest) -> Response:
        return self.controller.create(
            request=request
        )
