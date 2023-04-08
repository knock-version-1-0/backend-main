from rest_framework.request import HttpRequest
from rest_framework.response import Response
from core.service import BaseService
from core.crud import CRUDMixin


class BaseController(CRUDMixin):
    def __init__(self, service: BaseService):
        self.service = service

    def retrieve(self, request: HttpRequest, key: object) -> Response: ...

    def list(self, request: HttpRequest) -> Response: ...

    def create(self, request: HttpRequest) -> Response: ...

    def update(self, request: HttpRequest, key: object) -> Response: ...
