import pytest
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.fixtures import auth_client_fixture
from tests.factories.notes import make_notes
from core.utils.exceptions import get_error_name
from apps.notes.exceptions import (
    NoteDoesNotExistError,
)
from apps.users.exceptions import (
    UserInvalidError,
    UserPermissionError,
)


@pytest.mark.django_db
def test_200_OK(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]

    url = reverse('notes-detail', args=[note.displayId])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['data'] == note.dict()


@pytest.mark.django_db
def test_404_NoteDoesNotExistError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    url = reverse('notes-detail', args=[uuid.uuid4()])
    response = client.get(url)
    assert response.status_code == 404
    assert response.data['type'] == get_error_name(NoteDoesNotExistError())


@pytest.mark.django_db
def test_401_UserInvalidError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]

    user.is_active = False
    user.save()

    url = reverse('notes-detail', args=[note.displayId])
    response = client.get(url)
    assert response.status_code == 401
    assert response.data['type'] == get_error_name(UserInvalidError())


@pytest.mark.django_db
def test_403_UserPermissionError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    note = make_notes(author_id=user.id, size=1)[0]

    other = get_user_model().objects.create_user(username='other')
    set_credential(client, token=other.token)
    
    url = reverse('notes-detail', args=[note.displayId])
    response = client.get(url)
    assert response.status_code == 403
    assert response.data['type'] == get_error_name(UserPermissionError())
