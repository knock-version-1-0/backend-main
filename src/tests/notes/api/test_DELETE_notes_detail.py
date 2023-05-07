import pytest
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.fixtures import auth_client_fixture
from tests.factories.notes import make_notes
from core.utils.exceptions import get_error_name
from core import exceptions


@pytest.mark.django_db
def test_204_NO_CONTENT(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    notes = make_notes(user.id, size=5)
    
    note = notes.pop()
    url = reverse('notes-detail', args=[note.displayId])
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_404_NoteDoesNotExistError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    url = reverse('notes-detail', args=[uuid.uuid4()])
    response = client.delete(url)
    assert response.status_code == 404
    assert response.data['type'] == get_error_name(exceptions.notes.NoteDoesNotExistError())


@pytest.mark.django_db
def test_401_UserInvalidError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    notes = make_notes(user.id, size=5)
    note = notes.pop()
    user.is_active = False
    user.save()

    url = reverse('notes-detail', args=[note.displayId])
    response = client.delete(url)
    assert response.status_code == 401
    assert response.data['type'] == get_error_name(exceptions.users.UserInvalidError())


@pytest.mark.django_db
def test_403_UserPermissionError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    notes = make_notes(user.id, size=5)
    note = notes.pop()

    other = get_user_model().objects.create_user('other')
    set_credential(client, token=other.token)

    url = reverse('notes-detail', args=[note.displayId])
    response = client.delete(url)
    assert response.status_code == 403
    assert response.data['type'] == get_error_name(exceptions.users.UserPermissionError())
