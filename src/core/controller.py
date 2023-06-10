from rest_framework.request import Request as HttpRequest
from core.ws.request import Request as WsRequest
from rest_framework.response import Response as HttpResponse
from core.ws.response import Response as WsResponse

from core.service import BaseService
from core.crud import CRUDMixin


class HttpController(CRUDMixin):
    def __init__(self, service: BaseService):
        self.service = service

    def retrieve(self, request: HttpRequest, key: object) -> HttpResponse:
        raise NotImplementedError()

    def list(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError()

    def create(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError()

    def update(self, request: HttpRequest, key: object) -> HttpResponse:
        raise NotImplementedError()


class WsController(CRUDMixin):
    def __init__(self, service: BaseService):
        self.service = service

    def retrieve(self, request: WsRequest, key: object) -> WsResponse:
        raise NotImplementedError()

    def list(self, request: WsRequest) -> WsResponse:
        raise NotImplementedError()

    def create(self, request: WsRequest) -> WsResponse:
        raise NotImplementedError()

    def update(self, request: WsRequest, key: object) -> WsResponse:
        raise NotImplementedError()
