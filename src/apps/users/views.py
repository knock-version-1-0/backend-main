from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets


class AuthEmailViewSet(viewsets.ViewSet):
    controller = None

    def create(self, request: Request) -> Response:
        return self.controller.send_email(
            request=request
        )


class AuthVerificationViewSet(viewsets.ViewSet):
    controller = None

    def create(self, request: Request) -> Response:
        return self.controller.verify(
            request=request
        )


class AuthTokenViewSet(viewsets.ViewSet):
    controller = None

    def create(self, request: Request) -> Response:
        return self.controller.create(
            request=request
        )


class UserListViewSet(viewsets.ViewSet):
    controller = None

    def create(self, request: Request) -> Response:
        return self.controller.create(
            request=request
        )
