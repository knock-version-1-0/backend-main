import pytest
from django.urls import reverse

from tests.fixtures import auth_client_fixture
from tests.fixtures.notes import note_factory_fixture
from core.utils.exceptions import get_error_name
from core import exceptions
from adapters.dto.notes_dto import NoteReqDto
from core.models import StatusChoice


@pytest.mark.django_db
def test_201_CREATED(auth_client_fixture, note_factory_fixture):
    client, user, set_credential = auth_client_fixture

    req_dto = NoteReqDto(name='name', status=StatusChoice.SAVE)

    url = reverse('notes-list')
    response = client.post(url, req_dto.repr(), format='json')
    response_data = response.data['data']
    assert response.status_code == 201

    usecase = note_factory_fixture.usecase
    resp = usecase.retrieve(response_data['displayId'], user_id=user.id)
    assert response_data == resp


@pytest.mark.django_db
def test_400_NoteNameIntegrityError(auth_client_fixture):
    client, user, set_credential = auth_client_fixture

    req_dto = NoteReqDto(name='name', status=StatusChoice.SAVE)

    url = reverse('notes-list')
    response = client.post(url, req_dto.repr(), format='json')

    assert response.status_code == 201

    url = reverse('notes-list')
    response = client.post(url, req_dto.repr(), format='json')

    assert response.status_code == 400
    assert response.data['type'] == get_error_name(exceptions.notes.NoteNameIntegrityError())
