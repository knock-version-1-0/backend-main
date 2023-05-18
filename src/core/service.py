from typing import Tuple, Optional, Union
from rest_framework.request import QueryDict

from core.utils.exceptions import SomeError, get_error_name
from core.utils.typing import (
    StatusCode,
    make_error_detail,
    ErrorDetail,
)
from core.utils.data import ApiPayload
from core.usecase import BaseUsecase
from core.crud import CRUDMixin


class BaseService:
    def __init__(self, usecase: BaseUsecase):
        self.usecase = usecase

    def list(self, params: Optional[QueryDict]=None, **variables) -> Tuple[Union[ApiPayload, ErrorDetail], StatusCode]:
        raise NotImplementedError()

    def retrieve(self, key: object, **variables) -> Tuple[Union[ApiPayload, ErrorDetail], StatusCode]:
        raise NotImplementedError()

    def create(self, req_body: object, **variables) -> Tuple[Union[ApiPayload, ErrorDetail], StatusCode]:
        raise NotImplementedError()

    def update(self, key: object, req_body: object, **variables) -> Tuple[Union[ApiPayload, ErrorDetail], StatusCode]:
        raise NotImplementedError()
    
    def delete(self, key: object, **variables) -> Tuple[Union[ApiPayload, ErrorDetail], StatusCode]:
        raise NotImplementedError()


def error_wrapper(error: SomeError, status_code: StatusCode) -> Tuple[ErrorDetail, StatusCode]:
    return (make_error_detail(
        get_error_name(error),
        detail=error.args[0]
    ), status_code)
