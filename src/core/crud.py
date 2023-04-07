from typing import Optional, Type

from django.http.request import QueryDict


dto = object


class CRUDMixin:
    def list(self, query_param: Optional[QueryDict]=None, **variables):
        raise NotImplementedError()

    def retrieve(self, key: object, **variables):
        raise NotImplementedError()

    def create(self, req_body: dto, **variables):
        raise NotImplementedError()

    def update(self, key: object, req_body: dto, **variables):
        raise NotImplementedError()
