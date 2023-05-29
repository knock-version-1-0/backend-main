import pytest
from django.urls import reverse

from rest_framework.test import APIClient

from tests.factories.users import (
    email,
    timestamp
)
from core.utils.exceptions import get_error_name
from apps.users.exceptions import (
    EmailAddrValidationError
)
from adapters.dto.users_dto import (
    AuthEmailDto
)


@pytest.fixture(scope='module')
def auth_email_dto_fixture() -> AuthEmailDto:
    return AuthEmailDto(
        email=email,
        at=timestamp
    )


@pytest.mark.django_db
def test_200_OK(auth_email_dto_fixture):
    client = APIClient()
    dto: AuthEmailDto = auth_email_dto_fixture

    url = reverse('auth-email-list')
    response = client.post(url, dto.query_dict(), format='json')
    response_data = response.data['data']

    assert response.status_code == 200
    assert response_data['email'] == dto.email


@pytest.mark.django_db
def test_400_EmailAddrValidationError(auth_email_dto_fixture):
    client = APIClient()
    dto: AuthEmailDto = auth_email_dto_fixture
    dto = dto.copy(update={'email': 'invalidemail'})
    
    url = reverse('auth-email-list')
    response = client.post(url, dto.query_dict(), format='json')

    assert response.status_code == 400
    assert response.data['type'] == get_error_name(EmailAddrValidationError())
