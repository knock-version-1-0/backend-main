import pytest
from pydantic import BaseModel
from mixer.backend.django import mixer

from core.utils.pydantic import RequestBody
from core.utils.typing import Empty
from core.repository import BaseRepository
from apps.users.exceptions import (
    UserInvalidError,
)
from tests.fixtures.users import user_fixture


class Model(RequestBody):
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
    assert isinstance(model.b, Empty)


@pytest.mark.django_db
def test_is_user_authorized():
    """
    Call user from repository after authorize method is called
    """
    user = mixer.blend('users.User')

    repo = BaseRepository()
    assert repo.user == None

    repo.authorize(user.pk)
    assert bool(repo.user)


@pytest.mark.django_db
def test_repository_authorize(user_fixture):
    """
    Repository authorize method test
    """
    user_id = user_fixture.id
    repo = BaseRepository()
    repo.authorize(user_id)

    user_fixture.is_active = False
    user_fixture.save()
    with pytest.raises(UserInvalidError):
        repo.authorize(user_id)
    
    with pytest.raises(UserInvalidError):
        repo.authorize(2)
