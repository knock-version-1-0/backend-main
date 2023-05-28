from typing import TypeVar, Dict, Any, TypedDict

StatusCode = int
DTO = object
ID = TypeVar('ID')
LiteralData = Dict[str, Any]

class Empty:
    pass


TokenData = TypedDict('Token', {
    'id': ID,
    'exp': int,
    'at': int,
    'token_type': str
})
