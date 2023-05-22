from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework import viewsets


class EmailSendViewSet(viewsets.ViewSet):
    controller = None
    authentication_classes = []

    def create(self, request: HttpRequest) -> Response:
        return self.controller.send_email(
            request=request
        )
