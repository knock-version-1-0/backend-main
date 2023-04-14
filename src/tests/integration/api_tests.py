import uuid
import pytest
import faker

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from tests.fixtures import user_fixture, note_request_dto_fixture
from tests.factories import NoteModelFactory
from di.notes_factory import NoteFactory
from adapters.dto.notes_dto import (
    NoteReqDto,
)
from apps.notes.models import Note
from domains.constants import MAX_NOTE_LIST_LIMIT


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
    assert response.data['type'] == 'NoteDoesNotExistError'

    user_fixture.is_active = False
    user_fixture.save()
    url = reverse('notes-detail', args=[res_dto.displayId])
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['type'] == 'UserInvalidError'

    user2 = get_user_model().objects.create_user('user2')
    set_credential(client, token=user2.token)
    url = reverse('notes-detail', args=[res_dto.displayId])
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['type'] == 'UserPermissionError'


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


@pytest.mark.django_db
def test_GET_notes_list(user_fixture):
    client = APIClient()
    set_credential(client, token=user_fixture.token)

    size = 50
    notes = NoteModelFactory.create_batch(size=size)

    note_obj = notes[0]

    url = reverse('notes-list')
    response = client.get(url, {'name': note_obj.name})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == note_obj.name

    response = client.get(url, {'offset': 0})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == MAX_NOTE_LIST_LIMIT
    
    response = client.get(url, {'offset': 10, 'limit': 5})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5

    user_fixture.is_active = False
    user_fixture.save()
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['type'] == 'UserInvalidError'
