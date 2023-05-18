from typing import Optional, TypeVar
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class ErrorDetail:
    type: str
    message: Optional[str]=None


Data = TypeVar('Data')


@dataclass
class ApiPayload:
    status: str
    data: Data


class JwtToken(BaseModel):
    type: str
    value: str
