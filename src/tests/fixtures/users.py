import pytest
from typing import Tuple
import uuid

from rest_framework.test import APIClient

from apps.users.models import User
from domains.entities.users_entity import (
    UserEntity,
    AuthSessionEntity,
    AuthTokenEntity
)
from tests.factories.users import (
    email,
    make_users,
    emailCode,
    timestamp
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
        email=email
    )


@pytest.fixture
def auth_session_entity_fixture() -> AuthSessionEntity:
    return AuthSessionEntity(
        id=uuid.uuid4(),
        email=email,
        emailCode=emailCode,
        exp=timestamp + int(AuthSessionEntity.get_expire_period().total_seconds()),
        at=timestamp,
        attempt=0
    )


@pytest.fixture
def refresh_token_entity_fixture(user_entity_fixture) -> AuthTokenEntity:
    return AuthTokenEntity(
        type='refresh',
        value=user_entity_fixture.refreshToken.value
    )


@pytest.fixture
def access_token_entity_fixture(user_entity_fixture) -> AuthTokenEntity:
    return AuthTokenEntity(
        type='access',
        value=user_entity_fixture.accessToken.value
    )


def set_credential(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')


@pytest.fixture
def auth_client_fixture() -> Tuple[APIClient, User, set_credential]:
    client = APIClient()
    user_entity = make_users(size=1)

    set_credential(client, user_entity[0].accessToken.value)

    return (client, User.objects.get(pk=user_entity[0].id), set_credential)
