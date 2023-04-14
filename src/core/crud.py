from typing import Optional, Any

from django.http.request import QueryDict


class CRUDMixin:
    def list(self, params: Optional[QueryDict]=None, **variables):
        raise NotImplementedError()

    def retrieve(self, key: object, **variables) -> Any:
        raise NotImplementedError()

    def create(self, req_body: object, **variables) -> Any:
        raise NotImplementedError()

    def update(self, key: object, req_body: object, **variables) -> Any:
        raise NotImplementedError()
