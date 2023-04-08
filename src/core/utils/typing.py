from typing import Optional

StatusCode = int
Code = dict
DTO = object

def make_code(type: str, detail: Optional[str]=None) -> Code:
    return {
        'type': type,
        'message': detail,
    }
