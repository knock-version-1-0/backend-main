from typing import Tuple
import pytest
from rest_framework.test import APIClient
from apps.users.models import User


def set_credential(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')


@pytest.fixture
def auth_client_fixture() -> Tuple[APIClient, User, set_credential]:
    client = APIClient()
    user = User.objects.create_user('fixture_user')
    set_credential(client, user.token)

    return (client, user, set_credential)
