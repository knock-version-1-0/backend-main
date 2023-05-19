from typing import Tuple
import pytest
from rest_framework.test import APIClient
from apps.users.models import User
from domains.entities.users_entity import UserEntity


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
