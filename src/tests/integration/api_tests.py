import uuid

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.fixtures import user_fixture, note_request_dto_fixture
from di.notes_factory import NoteFactory
from adapters.dto.notes_dto import (
    NoteReqDto,
)
from django.contrib.auth import get_user_model


def set_credential(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')


@pytest.mark.django_db
def test_GET_notes_detail(user_fixture, note_request_dto_fixture):
    client = APIClient()
    set_credential(client, token=user_fixture.token)

    usecase = NoteFactory().usecase
    res_dto = usecase.create(
        note_request_dto_fixture,
        user_id=user_fixture.id
    )
    url = reverse('notes-detail', args=[res_dto.displayId])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == res_dto.dict()

    url = reverse('notes-detail', args=[uuid.uuid4()])
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    user_fixture.is_active = False
    user_fixture.save()

    url = reverse('notes-detail', args=[res_dto.displayId])
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    user2 = get_user_model().objects.create_user('user2')
    set_credential(client, token=user2.token)

    url = reverse('notes-detail', args=[res_dto.displayId])
    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_POST_notes_list(user_fixture, note_request_dto_fixture):
    client = APIClient()
    set_credential(client, token=user_fixture.token)

    req_dto = note_request_dto_fixture
    url = reverse('notes-list')
    response = client.post(url, req_dto.dict(), format='json')

    assert response.status_code == status.HTTP_200_OK
    usecase = NoteFactory().usecase
    res_dto = usecase.retrieve(response.data['displayId'], user_id=user_fixture.id)
    assert response.data == res_dto.dict()

    response = client.post(url, req_dto.dict(), format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['type'] == 'NoteNameIntegrityError'

    data = req_dto.dict()
    data['name'] = req_dto.name + '1'
    data['keywords'] = [{'posId': 1} for _ in range(4)]
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['type'] == 'KeywordPosIdIntegrityError'
