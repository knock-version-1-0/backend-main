import pytest
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.fixtures import auth_client_fixture
from tests.factories.notes import make_notes
from core.utils.exceptions import get_error_name
from apps.notes.exceptions import (
    NoteNameIntegrityError,
    NoteNameLengthLimitError,
    NoteDoesNotExistError
)
from apps.users.exceptions import (
    UserInvalidError,
    UserPermissionError,
)
from core.models import StatusChoice
from adapters.dto.notes_dto import NoteDto
from domains.constants import NOTE_NAME_LENGTH_LIMIT
from domains.entities.users_entity import UserEntity


@pytest.mark.django_db
def test_200_OK(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]

    changed_name = 'note_changed_name'
    req_dto = NoteDto(name=changed_name)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.query_dict(), format='json')
    response_data = response.data['data']

    assert response.status_code == 200

    for key, value in note.dict().items():
        if key == 'name':
            assert response_data[key] == changed_name
        else:
            assert response_data[key] == value

    req_dto = NoteDto(status=StatusChoice.EXPIRE)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.query_dict(), format='json')
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

    req_dto = NoteDto(name=changed_name)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.query_dict(), format='json')
    assert response.status_code == 200

    note = make_notes(author_id=user.id, size=1)[0]

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.query_dict(), format='json')
    assert response.status_code == 400
    assert response.data['type'] == get_error_name(NoteNameIntegrityError())


@pytest.mark.django_db
def test_400_NoteNameLengthLimitError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]
    req_dto = NoteDto(name='n' * (NOTE_NAME_LENGTH_LIMIT+1))

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.query_dict(), format='json')
    assert response.status_code == 400
    assert response.data['type'] == get_error_name(NoteNameLengthLimitError())


@pytest.mark.django_db
def test_404_NoteDoesNotExistError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    changed_name = 'note_changed_name'
    req_dto = NoteDto(name=changed_name)

    url = reverse('notes-detail', args=[uuid.uuid4()])
    response = client.patch(url, data=req_dto.query_dict(), format='json')

    assert response.status_code == 404
    assert response.data['type'] == get_error_name(NoteDoesNotExistError())


@pytest.mark.django_db
def test_401_UserInvalidError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]

    user.is_active = False
    user.save()

    changed_name = 'note_changed_name'
    req_dto = NoteDto(name=changed_name)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.query_dict(), format='json')
    assert response.status_code == 401
    assert response.data['type'] == get_error_name(UserInvalidError())


@pytest.mark.django_db
def test_403_UserPermissionError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]

    other = get_user_model().objects.create_user('other')
    other_entity = UserEntity(
        id=other.pk,
        username=other.username,
        email='other.email@email.com',
        isActive=other.is_active,
        isStaff=other.is_staff
    )
    set_credential(client, token=other_entity.accessToken.value)

    changed_name = 'note_changed_name'
    req_dto = NoteDto(name=changed_name)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.patch(url, data=req_dto.query_dict(), format='json')
    assert response.status_code == 403
    assert response.data['type'] == get_error_name(UserPermissionError())
