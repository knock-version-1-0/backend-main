import uuid
import pytest
from typing import Tuple
from datetime import datetime

from rest_framework.test import APIClient

from apps.users.models import User
from domains.entities.users_entity import (
    UserEntity,
    AuthSessionEntity,
)
from adapters.dto.users_dto import (
    AuthEmailDto,
    AuthVerificationDto
)
from tests.factories.users import email, timestamp, make_users


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


def set_credential(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')


@pytest.fixture
def auth_client_fixture() -> Tuple[APIClient, User, set_credential]:
    client = APIClient()
    user_entity = make_users(size=1)

    set_credential(client, user_entity[0].accessToken.value)

    return (client, User.objects.get(pk=user_entity[0].id), set_credential)


@pytest.fixture
def auth_email_dto_fixture() -> AuthEmailDto:
    return AuthEmailDto(
        email=email,
        at=timestamp
    )


@pytest.fixture
def auth_verification_dto_fixture() -> AuthVerificationDto:
    return AuthVerificationDto(
        id=uuid.uuid4(),
        email=email,
        emailCode='660011',
        currentTime=timestamp
    )
