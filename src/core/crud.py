from typing import Optional, Any
from rest_framework.request import QueryDict


class CRUDMixin:
    def list(self, params: Optional[QueryDict]=None, **variables) -> Any:
        raise NotImplementedError()

    def retrieve(self, key: object, **variables) -> Any:
        raise NotImplementedError()

    def create(self, req_body: object, **variables) -> Any:
        raise NotImplementedError()

    def update(self, key: object, req_body: object, **variables) -> Any:
        raise NotImplementedError()
    
    def delete(self, key: object, **variables) -> None:
        raise NotImplementedError()
