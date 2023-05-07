import pytest
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.fixtures import auth_client_fixture
from tests.factories.notes import make_notes
from core.utils.exceptions import get_error_name
from core import exceptions
from core.models import StatusChoice
from adapters.dto.notes_dto import NoteReqDto
from domains.constants import NOTE_NAME_LENGTH_LIMIT


@pytest.mark.django_db
def test_200_OK(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]

    changed_name = 'note_changed_name'
    req_dto = NoteReqDto(name=changed_name)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.data(), format='json')
    response_data = response.data['data']

    assert response.status_code == 200

    for key, value in note.dict().items():
        if key == 'name':
            assert response_data[key] == changed_name
        else:
            assert response_data[key] == value

    req_dto = NoteReqDto(status=StatusChoice.EXPIRE)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.data(), format='json')
    response_data = response.data['data']

    assert response.status_code == 200

    for key, value in note.dict().items():
        if key == 'status':
            assert response_data[key] == StatusChoice.EXPIRE
        elif key == 'name':
            assert response_data[key] == changed_name
        else:
            assert response_data[key] == value


@pytest.mark.django_db
def test_400_NoteNameIntegrityError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]
    changed_name = 'note_changed_name'

    req_dto = NoteReqDto(name=changed_name)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.data(), format='json')
    assert response.status_code == 200

    note = make_notes(author_id=user.id, size=1)[0]

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.data(), format='json')
    assert response.status_code == 400
    assert response.data['type'] == get_error_name(exceptions.notes.NoteNameIntegrityError())


@pytest.mark.django_db
def test_400_NoteNameLengthLimitError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]
    req_dto = NoteReqDto(name='n' * (NOTE_NAME_LENGTH_LIMIT+1))

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.data(), format='json')
    assert response.status_code == 400
    assert response.data['type'] == get_error_name(exceptions.notes.NoteNameLengthLimitError(NOTE_NAME_LENGTH_LIMIT))


@pytest.mark.django_db
def test_404_NoteDoesNotExistError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    changed_name = 'note_changed_name'
    req_dto = NoteReqDto(name=changed_name)

    url = reverse('notes-detail', args=[uuid.uuid4()])
    response = client.patch(url, data=req_dto.data(), format='json')

    assert response.status_code == 404
    assert response.data['type'] == get_error_name(exceptions.notes.NoteDoesNotExistError())


@pytest.mark.django_db
def test_401_UserInvalidError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]

    user.is_active = False
    user.save()

    changed_name = 'note_changed_name'
    req_dto = NoteReqDto(name=changed_name)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.data(), format='json')
    assert response.status_code == 401
    assert response.data['type'] == get_error_name(exceptions.users.UserInvalidError())


@pytest.mark.django_db
def test_403_UserPermissionError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]

    other = get_user_model().objects.create_user('other')
    set_credential(client, token=other.token)

    changed_name = 'note_changed_name'
    req_dto = NoteReqDto(name=changed_name)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.data(), format='json')
    assert response.status_code == 403
    assert response.data['type'] == get_error_name(exceptions.users.UserPermissionError())
