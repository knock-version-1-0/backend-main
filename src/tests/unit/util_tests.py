import pytest
from pydantic import BaseModel

from core.utils.pydantic import RequestBody


class Model(RequestBody, BaseModel):
    a: str
    b: int
    c: int


@pytest.mark.unit
def test_request_body():
    model = Model(
        a='str'
    )
