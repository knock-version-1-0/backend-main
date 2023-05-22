from rest_framework.request import HttpRequest
from rest_framework.response import Response
from dataclasses import asdict
from core.controller import BaseController

from adapters.services.users_service import (
    AuthService,
)

__all__ = [
    'AuthService',
]


class AuthController(BaseController):

    def __init__(self, service: AuthService):
        self.service = service
    
    def send_email(self, request: HttpRequest) -> Response:
        payload, status = self.service.send_email(request.data)

        return Response(asdict(payload), status=status)
