import pytest
from pydantic import BaseModel

from core.utils.pydantic import RequestBody
from core.utils.typing import Empty


class Model(RequestBody, BaseModel):
    a: str
    b: int
    c: int


@pytest.mark.unit
def test_request_body():
    model = Model(
        a='str'
    )

    assert model.a == 'str'
    assert isinstance(model.a, str)
    assert model.b == Empty
    assert isinstance(model.b, Empty)
