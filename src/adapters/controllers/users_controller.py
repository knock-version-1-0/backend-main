from rest_framework.request import HttpRequest
from rest_framework.response import Response
from dataclasses import asdict
from core.controller import BaseController

from adapters.services.users_service import (
    AuthService,
    UserService
)


class AuthController(BaseController):

    def __init__(self, service: AuthService):
        self.service = service
    
    def send_email(self, request: HttpRequest) -> Response:
        payload, status = self.service.send_email(request.data)

        return Response(asdict(payload), status=status)
    
    def verify(self, request: HttpRequest) -> Response:
        payload, status = self.service.verify(request.data)

        return Response(asdict(payload), status=status)


class UserController(BaseController):

    def __init__(self, service: UserService):
        self.service = service
    
    def create(self, request: HttpRequest) -> Response:
        payload, status = self.service.create(request.data)

        return Response(asdict(payload), status=status)
