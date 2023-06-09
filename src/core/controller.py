import json
from django.http.request import QueryDict
from rest_framework.request import Request
from rest_framework.response import Response
from core.service import BaseService
from core.crud import CRUDMixin


class HttpController(CRUDMixin):
    def __init__(self, service: BaseService):
        self.service = service

    def retrieve(self, request: Request, key: object) -> Response: ...

    def list(self, request: Request) -> Response: ...

    def create(self, request: Request) -> Response: ...

    def update(self, request: Request, key: object) -> Response: ...


class WsController(CRUDMixin):
    def __init__(self, service: BaseService):
        self.service = service

    def retrieve(self, event, key: object) -> str: ...

    def list(self, event) -> str: ...

    def create(self, event) -> str: ...

    def update(self, event, key: object) -> str: ...

    def _parse(self, event) -> QueryDict:
        message = event["message"]
        data = json.loads(message)
        query_dict = QueryDict('', mutable=True)
        query_dict.update(data)
        return query_dict
