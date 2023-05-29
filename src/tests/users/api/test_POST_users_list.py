import pytest
from django.urls import reverse

from rest_framework.test import APIClient


@pytest.mark.django_db
def test_201_CREATED():
    client = APIClient()

    url = reverse('users-list')
    response = client.post(url, {'email': 'email@test.com'}, format='json')
    assert response.status_code == 201

    response = client.post(url, {'email': 'email@test.com'}, format='json')
    assert response.status_code == 201
