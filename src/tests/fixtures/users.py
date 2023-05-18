import pytest
import uuid
import datetime

from apps.users.models import User
from domains.entities.users_entity import (
    UserEntity,
    AuthSessionEntity,
)


@pytest.fixture
def user_fixture() -> User:
    user = User.objects.create_user('fixture_user')
    return user


@pytest.fixture
def user_entity_fixture() -> UserEntity:
    return UserEntity(
        id=1,
        username='user_name',
        isActive=True,
        isStaff=False,
        email='user_name@email.com'
    )
