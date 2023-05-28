import pytest
from django.urls import reverse

from rest_framework.test import APIClient

from core.utils.exceptions import get_error_name
from apps.users.exceptions import (
    EmailAddrValidationError
)
from domains.entities.users_entity import (
    AuthSessionEntity
)


@pytest.mark.django_db
def test_201_CREATED():
    client = APIClient()

    url = reverse('users-list')
    response = client.post(url, {'email': 'email@test.com'}, format='json')
    assert response.status_code == 201

    response = client.post(url, {'email': 'email@test.com'}, format='json')
    assert response.status_code == 201
