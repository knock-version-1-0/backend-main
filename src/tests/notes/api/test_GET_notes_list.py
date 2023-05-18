import pytest
from django.urls import reverse

from tests.fixtures import auth_client_fixture
from tests.factories.notes import make_notes
from core.utils.exceptions import get_error_name
from apps.users.exceptions import UserInvalidError
from domains.constants import MAX_NOTE_LIST_LIMIT


@pytest.mark.django_db
def test_200_OK(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    size = 50
    notes = make_notes(author_id=user.id, size=size)

    note = notes[0]

    url = reverse('notes-list')
    response = client.get(url, {'name': note.name})
    response_data = response.data['data']

    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]['name'] == note.name

    response = client.get(url, {'offset': 0})
    response_data = response.data['data']

    assert response.status_code == 200
    assert len(response_data) == MAX_NOTE_LIST_LIMIT
    
    response = client.get(url, {'offset': 10, 'limit': 5})
    response_data = response.data['data']

    assert response.status_code == 200
    assert len(response_data) == 5


@pytest.mark.django_db
def test_401_UserInvalidError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    user.is_active = False
    user.save()

    url = reverse('notes-list')
    response = client.get(url)
    assert response.status_code == 401
    assert response.data['type'] == get_error_name(UserInvalidError())
