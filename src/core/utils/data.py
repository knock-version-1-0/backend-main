from typing import Optional, TypeVar
from dataclasses import dataclass


@dataclass
class ErrorDetail:
    type: str
    message: Optional[str]=None


def make_error_detail(type: str, detail: Optional[str]=None) -> ErrorDetail:
    return ErrorDetail(type=type, message=detail)


Data = TypeVar('Data')


@dataclass
class ApiPayload:
    status: str
    data: Data
