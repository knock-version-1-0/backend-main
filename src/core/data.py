from typing import Optional, TypeVar
from dataclasses import dataclass


@dataclass
class ErrorDetail:
    type: str
    message: Optional[str]=None


Data = TypeVar('Data')

@dataclass
class ApiPayload:
    status: str
    data: Data
