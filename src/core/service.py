from typing import Tuple

from core.utils.exceptions import SomeError, get_error_name
from core.utils.typing import StatusCode, make_error_detail, ErrorDetail
from core.usecase import BaseUsecase
from core.crud import CRUDMixin


class BaseService(CRUDMixin):
    def __init__(self, usecase: BaseUsecase):
        self.usecase = usecase


def error_wrapper(error: SomeError, status_code: StatusCode) -> Tuple[ErrorDetail, StatusCode]:
    return (make_error_detail(
        get_error_name(error),
        detail=error.args[0]
    ), status_code)
