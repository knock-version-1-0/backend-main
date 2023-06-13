import pytest

from django.urls import reverse

from tests.fixtures.users import auth_client_fixture
from core.utils.exceptions import get_error_name
from apps.users.exceptions import UserInvalidError


@pytest.mark.django_db
def test_200_OK(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    url = reverse('users-me-list')
    response = client.get(url)
    response_data = response.data['data']

    assert response.status_code == 200
    assert response_data['id'] == user.pk


@pytest.mark.django_db
def test_401_UserInvalidError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    user.is_active = False
    user.save()

    url = reverse('users-me-list')
    response = client.get(url)

    assert response.status_code == 401
    assert response.data['type'] == get_error_name(UserInvalidError())
