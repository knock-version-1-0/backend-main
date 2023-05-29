from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework import viewsets


class AuthEmailViewSet(viewsets.ViewSet):
    controller = None
    authentication_classes = []

    def create(self, request: HttpRequest) -> Response:
        return self.controller.send_email(
            request=request
        )


class AuthVerificationViewSet(viewsets.ViewSet):
    controller = None
    authentication_classes = []

    def create(self, request: HttpRequest) -> Response:
        return self.controller.verify(
            request=request
        )


class UserListViewSet(viewsets.ViewSet):
    controller = None
    authentication_classes = []

    def create(self, request: HttpRequest) -> Response:
        return self.controller.create(
            request=request
        )
