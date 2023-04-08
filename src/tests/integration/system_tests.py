import pytest
from mixer.backend.django import mixer

from tests.fixtures import (
    user_fixture,
)

from core.repository import BaseRepository
from domains.exceptions import (
    AuthorizeNotCalledError,
    RepositoryAuthorizeError
)


@pytest.mark.django_db
def test_is_user_authorized():
    """
    Call user from repository after authorize method is called
    """
    user = mixer.blend('users.User')

    repo = BaseRepository()
    with pytest.raises(AuthorizeNotCalledError.type):
        repo.user

    repo.authorize(user.pk)
    repo.user


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
    with pytest.raises(RepositoryAuthorizeError):
        repo.authorize(user_id)
    
    with pytest.raises(RepositoryAuthorizeError):
        repo.authorize(2)
