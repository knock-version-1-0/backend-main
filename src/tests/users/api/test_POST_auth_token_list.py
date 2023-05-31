import pytest
from datetime import datetime

from django.urls import reverse
from rest_framework.test import APIClient

from tests.factories.users import make_users
from core.utils.exceptions import get_error_name
from apps.users.exceptions import (
    RefreshTokenExpired,
    RefreshTokenRequired,
    UserInvalidError
)
from adapters.dto.users_dto import (
    AuthTokenDto
)
from core.utils.jwt import parse_jwt_token, generate_jwt_token
from di.users_factory import UserFactory


@pytest.fixture(scope='function')
def api_client():
    client = APIClient()
    client.credentials(HTTP_CACHE_CONTROL="public, max-age=1800", HTTP_USER_AGENT='ClearCache')
    return client


@pytest.mark.django_db
def test_200_OK(api_client):
    client: APIClient = api_client
    user_entity = make_users(size=1)[0]
    refresh_token = user_entity.refreshToken.value
    dto = AuthTokenDto(type='refresh', value=refresh_token)

    url = reverse('auth-token-list')
    response = client.post(url, dto.query_dict(), format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_400_RefreshTokenRequired(api_client):
    client: APIClient = api_client
    user_entity = make_users(size=1)[0]
    refresh_token = user_entity.refreshToken.value
    dto = AuthTokenDto(type='other', value=refresh_token)

    url = reverse('auth-token-list')
    response = client.post(url, dto.query_dict(), format='json')
    assert response.status_code == 400
    assert response.data['type'] == get_error_name(RefreshTokenRequired())


@pytest.mark.django_db
def test_400_RefreshTokenExpired(api_client):
    client: APIClient = api_client
    user_entity = make_users(size=1)[0]
    refresh_token = user_entity.refreshToken.value
    data = parse_jwt_token(refresh_token)
    data['exp'] = int(datetime.now().strftime('%s')) - 1000
    refresh_token = generate_jwt_token(
        id=data['id'],
        exp=data['exp'],
        at=data['at'],
        type=data['token_type']
    )

    dto = AuthTokenDto(type='refresh', value=refresh_token)

    url = reverse('auth-token-list')
    response = client.post(url, dto.query_dict(), format='json')

    assert response.status_code == 400
    assert response.data['type'] == get_error_name(RefreshTokenExpired())


@pytest.mark.django_db
def test_401_UserInvalidError(api_client):
    client: APIClient = api_client
    user_entity = make_users(size=1)[0]
    repository = UserFactory().repository
    repository.find_by_id(user_entity.id)
    repository.delete()

    refresh_token = user_entity.refreshToken.value
    dto = AuthTokenDto(type='refresh', value=refresh_token)

    url = reverse('auth-token-list')
    response = client.post(url, dto.query_dict(), format='json')
    assert response.status_code == 401
    assert response.data['type'] == get_error_name(UserInvalidError())
