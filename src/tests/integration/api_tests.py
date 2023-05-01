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
from apps.notes.models import Note
from domains.constants import MAX_NOTE_LIST_LIMIT, NOTE_NAME_LENGTH_LIMIT
from core.models import StatusChoice
from core.exceptions import (
    NoteDoesNotExistError,
    UserInvalidError,
    UserPermissionError,
    NoteNameIntegrityError,
    NoteNameLengthLimitError
)
from core.utils.exceptions import get_error_name


def set_credential(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')


@pytest.mark.django_db
def test_GET_notes_detail(user_fixture, note_request_dto_fixture):
    client = APIClient()
    set_credential(client, token=user_fixture.token)

    usecase = NoteFactory().usecase
    resp = usecase.create(
        note_request_dto_fixture,
        user_id=user_fixture.id
    )
    display_id = resp['displayId']

    url = reverse('notes-detail', args=[display_id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == resp

    url = reverse('notes-detail', args=[uuid.uuid4()])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['type'] == get_error_name(NoteDoesNotExistError())

    user_fixture.is_active = False
    user_fixture.save()
    url = reverse('notes-detail', args=[display_id])
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['type'] == get_error_name(UserInvalidError())

    user2 = get_user_model().objects.create_user('user2')
    set_credential(client, token=user2.token)
    url = reverse('notes-detail', args=[display_id])
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['type'] == get_error_name(UserPermissionError())


@pytest.mark.django_db
def test_POST_notes_list(user_fixture, note_request_dto_fixture):
    client = APIClient()
    set_credential(client, token=user_fixture.token)

    req_dto = note_request_dto_fixture
    url = reverse('notes-list')
    response = client.post(url, req_dto.dict(), format='json')

    assert response.status_code == status.HTTP_201_CREATED
    usecase = NoteFactory().usecase
    resp = usecase.retrieve(response.data['displayId'], user_id=user_fixture.id)
    assert response.data == resp

    response = client.post(url, req_dto.dict(), format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['type'] == get_error_name(NoteNameIntegrityError())


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
    assert response.data['type'] == get_error_name(UserInvalidError())


@pytest.mark.django_db
def test_DELETE_notes_list(user_fixture):
    client = APIClient()
    set_credential(client, token=user_fixture.token)

    notes = NoteModelFactory.create_batch(size=5)
    
    note = notes.pop()
    url = reverse('notes-detail', args=[note.display_id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    url = reverse('notes-detail', args=[uuid.uuid4()])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['type'] == get_error_name(NoteDoesNotExistError())

    note = notes.pop()
    url = reverse('notes-detail', args=[note.display_id])
    user_fixture.is_active = False
    user_fixture.save()
    response = client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['type'] == get_error_name(UserInvalidError())

    note = notes.pop()
    url = reverse('notes-detail', args=[note.display_id])
    user2 = get_user_model().objects.create_user('user2')
    set_credential(client, token=user2.token)
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['type'] == get_error_name(UserPermissionError())


@pytest.mark.django_db
def test_PATCH_notes_detail(user_fixture, note_request_dto_fixture):
    client = APIClient()
    set_credential(client, token=user_fixture.token)

    usecase = NoteFactory().usecase
    resp = usecase.create(
        note_request_dto_fixture,
        user_id=user_fixture.id
    )
    display_id = resp['displayId']

    changed_name = 'note_name1'
    req_data = {
        'name': changed_name
    }
    url = reverse('notes-detail', args=[display_id])
    response = client.patch(url, data=req_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    for key, value in resp.items():
        if key == 'name':
            assert response.data[key] == changed_name
        else:
            assert response.data[key] == value

    req_data = {
        'status': StatusChoice.EXPIRE
    }
    url = reverse('notes-detail', args=[display_id])
    response = client.patch(url, data=req_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    for key, value in resp.items():
        if key == 'status':
            assert response.data[key] == StatusChoice.EXPIRE
        elif key == 'name':
            assert response.data[key] == changed_name
        else:
            assert response.data[key] == value

    usecase = NoteFactory().usecase
    resp = usecase.create(
        note_request_dto_fixture,
        user_id=user_fixture.id
    )
    display_id = resp['displayId']

    req_data = {
        'name': changed_name
    }
    url = reverse('notes-detail', args=[display_id])
    response = client.patch(url, data=req_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['type'] == get_error_name(NoteNameIntegrityError())

    req_data = {
        'name': 'n' * (NOTE_NAME_LENGTH_LIMIT+1)
    }
    url = reverse('notes-detail', args=[display_id])
    response = client.patch(url, data=req_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['type'] == get_error_name(NoteNameLengthLimitError(NOTE_NAME_LENGTH_LIMIT))

    req_data = {
        'name': 'new name 1'
    }
    url = reverse('notes-detail', args=[uuid.uuid4()])
    response = client.patch(url, data=req_data, format='json')
    print(response.data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['type'] == get_error_name(NoteDoesNotExistError())

    user_fixture.is_active = False
    user_fixture.save()
    url = reverse('notes-detail', args=[display_id])
    response = client.patch(url, data=req_data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['type'] == get_error_name(UserInvalidError())

    user2 = get_user_model().objects.create_user('user2')
    set_credential(client, token=user2.token)
    url = reverse('notes-detail', args=[display_id])
    response = client.patch(url, data=req_data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['type'] == get_error_name(UserPermissionError())
