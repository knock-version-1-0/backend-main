from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework import status as http_status
from dataclasses import asdict

from core.controller import BaseController

from adapters.services.users_service import (
    AuthSessionService,
    UserService,
    AuthTokenService
)
from core.views import parse_max_age
from core.utils.data import ErrorDetail


class AuthSessionController(BaseController):

    def __init__(self, service: AuthSessionService):
        self.service = service
    
    def send_email(self, request: HttpRequest) -> Response:
        payload, status = self.service.send_email(request.data)

        return Response(asdict(payload), status=status)
    
    def verify(self, request: HttpRequest) -> Response:
        payload, status = self.service.verify(request.data)

        return Response(asdict(payload), status=status)


class AuthTokenController(BaseController):

    def __init__(self, service: AuthTokenService):
        self.service = service
    
    def create(self, request: HttpRequest) -> Response:
        cache_control_header = request.META.get('HTTP_CACHE_CONTROL')
        max_age = None

        if cache_control_header:
            max_age = parse_max_age(cache_control_header)

        if max_age is None:
            data = ErrorDetail(type='BAD_REQUEST', message='Client have to set cache control header with max-age value')
            return Response(asdict(data), status=http_status.HTTP_400_BAD_REQUEST)
        
        user_agent = request.META.get('HTTP_USER_AGENT')
        if user_agent == 'ClearCache':
            from django.core.cache import cache
            cache.delete('auth/token')

        payload, status = self.service.create(data=request.data, max_age=max_age)

        response = Response(asdict(payload), status=status)
        response['Cache-Control'] = 'no-cache, must-revalidate'

        return response


class UserController(BaseController):

    def __init__(self, service: UserService):
        self.service = service
    
    def create(self, request: HttpRequest) -> Response:
        payload, status = self.service.create(request.data)

        return Response(asdict(payload), status=status)
    
    def me(self, request: HttpRequest) -> Response:
        payload, status = self.service.me(user_id=request.user.pk)

        return Response(asdict(payload), status=status)
