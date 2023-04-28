from typing import Optional

StatusCode = int
DTO = object

def make_code(type: str, detail: Optional[str]=None) -> dict:
    return {
        'type': type,
        'message': detail,
    }
