import pytest
from django.urls import reverse
import uuid

from rest_framework.test import APIClient

from tests.factories.users import make_auth_sessions
from core.utils.exceptions import get_error_name
from apps.users.exceptions import (
    AttemptLimitOver,
    AuthSessionExpired,
    AuthenticationFailed,
    AuthSessionDoesNotExist
)
from adapters.dto.users_dto import (
    AuthVerificationDto
)
from domains.entities.users_entity import AuthSessionEntity


@pytest.fixture(scope='module')
def client_fixture():
    return APIClient()


@pytest.fixture
def auth_session_fixture():
    return make_auth_sessions(size=1)[0]


@pytest.mark.django_db
def test_200_OK(client_fixture, auth_session_fixture):
    client: APIClient = client_fixture
    auth_session: AuthSessionEntity = auth_session_fixture
    dto = AuthVerificationDto(
        id=auth_session.id,
        email=auth_session.email,
        emailCode=auth_session.emailCode,
        currentTime=auth_session.at + 1
    )

    url = reverse('auth-verification-list')
    response = client.post(url, dto.query_dict(), format='json')
    
    assert response.status_code == 200


@pytest.mark.django_db
def test_400_AttemptLimitOver(client_fixture, auth_session_fixture):
    client: APIClient = client_fixture
    auth_session: AuthSessionEntity = auth_session_fixture
    dto = AuthVerificationDto(
        id=auth_session.id,
        email=auth_session.email,
        emailCode='0'*6 if auth_session.emailCode != '0'*6 else '1'*6,
        currentTime=auth_session.at + 1
    )
    
    url = reverse('auth-verification-list')
    response = client.post(url, dto.query_dict(), format='json')
    assert response.status_code == 401
    response = client.post(url, dto.query_dict(), format='json')
    assert response.status_code == 401
    response = client.post(url, dto.query_dict(), format='json')

    assert response.status_code == 400
    assert response.data['type'] == get_error_name(AttemptLimitOver())


@pytest.mark.django_db
def test_400_AuthSessionExpired(client_fixture, auth_session_fixture):
    client: APIClient = client_fixture
    auth_session: AuthSessionEntity = auth_session_fixture
    dto = AuthVerificationDto(
        id=auth_session.id,
        email=auth_session.email,
        emailCode=auth_session.emailCode,
        currentTime=auth_session.exp + 1
    )

    url = reverse('auth-verification-list')
    response = client.post(url, dto.query_dict(), format='json')

    assert response.status_code == 400
    assert response.data['type'] == get_error_name(AuthSessionExpired())


@pytest.mark.django_db
def test_401_AuthenticationFailed(client_fixture, auth_session_fixture):
    client: APIClient = client_fixture
    auth_session: AuthSessionEntity = auth_session_fixture
    dto = AuthVerificationDto(
        id=auth_session.id,
        email=auth_session.email,
        emailCode='0'*6 if auth_session.emailCode != '0'*6 else '1'*6,
        currentTime=auth_session.at + 1
    )

    url = reverse('auth-verification-list')
    response = client.post(url, dto.query_dict(), format='json')

    assert response.status_code == 401
    assert response.data['type'] == get_error_name(AuthenticationFailed())


@pytest.mark.django_db
def test_404_AuthSessionDoesNotExist(client_fixture, auth_session_fixture):
    client: APIClient = client_fixture
    auth_session: AuthSessionEntity = auth_session_fixture
    dto = AuthVerificationDto(
        id=auth_session.id,
        email=auth_session.email,
        emailCode=auth_session.emailCode,
        currentTime=auth_session.at + 1
    )

    dto = dto.copy(update={'id': uuid.uuid4()})

    url = reverse('auth-verification-list')
    response = client.post(url, dto.query_dict(), format='json')

    assert response.status_code == 404
    assert response.data['type'] == get_error_name(AuthSessionDoesNotExist())

    dto = dto.copy(update={'email': 'other'+auth_session.email})

    url = reverse('auth-verification-list')
    response = client.post(url, dto.query_dict(), format='json')

    assert response.status_code == 404
    assert response.data['type'] == get_error_name(AuthSessionDoesNotExist())
