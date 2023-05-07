from typing import Optional
from core.data import ErrorDetail

StatusCode = int
DTO = object

def make_error_detail(type: str, detail: Optional[str]=None) -> ErrorDetail:
    return ErrorDetail(type=type, message=detail)

class Empty:
    pass
