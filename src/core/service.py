from typing import Tuple, Optional, Union
from rest_framework.request import QueryDict

from core.utils.exceptions import SomeError, get_error_name
from core.utils.typing import (
    StatusCode,
)
from core.utils.data import (
    ErrorDetail,
    make_error_detail,
    ApiPayload
)
from core.usecase import BaseUsecase
from core.crud import CRUDMixin


class BaseService:
    def __init__(self, usecase: BaseUsecase):
        self.usecase = usecase

    def list(self, params: Optional[QueryDict]=None, **variables) -> Tuple[Union[ApiPayload, ErrorDetail], int]:
        raise NotImplementedError()

    def retrieve(self, key: object, **variables) -> Tuple[Union[ApiPayload, ErrorDetail], int]:
        raise NotImplementedError()

    def create(self, data: QueryDict, **variables) -> Tuple[Union[ApiPayload, ErrorDetail], int]:
        raise NotImplementedError()

    def update(self, key: object, data: QueryDict, **variables) -> Tuple[Union[ApiPayload, ErrorDetail], int]:
        raise NotImplementedError()
    
    def delete(self, key: object, **variables) -> Tuple[Union[ApiPayload, ErrorDetail], int]:
        raise NotImplementedError()


def error_wrapper(error: SomeError, status_code: StatusCode) -> Tuple[ErrorDetail, int]:
    return (make_error_detail(
        get_error_name(error),
        detail=error.args[0]
    ), status_code)
