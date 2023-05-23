import pytest
from typing import Tuple
from rest_framework.test import APIClient

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


def set_credential(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')


@pytest.fixture
def auth_client_fixture() -> Tuple[APIClient, User, set_credential]:
    client = APIClient()
    user = User.objects.create_user('fixture_user')
    user_entity = UserEntity(
        id=user.pk,
        username=user.username,
        email='user.email@email.com',
        isActive=user.is_active,
        isStaff=user.is_staff
    )
    set_credential(client, user_entity.accessToken.value)

    return (client, user, set_credential)
