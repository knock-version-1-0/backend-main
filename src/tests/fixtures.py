import time
from typing import List, Tuple
import uuid
import pytest
from rest_framework.test import APIClient

from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity,
    NoteSummaryEntity
)
from adapters.dto.notes_dto import (
    NoteReqDto,
    KeywordReqDto,
)
from core.models import StatusChoice
from domains.entities.notes_entity import KeywordStatus
from apps.users.models import User
from di.notes_factory import NoteFactory


@pytest.fixture
def note_entity_fixture() -> NoteEntity:
    return NoteEntity(
        id=1,
        authorId=1,
        displayId=uuid.uuid4(),
        name='note1',
        keywords=[KeywordEntity(
            id=i+1,
            noteId=i+1,
            posX=i * 10,
            posY=i * 10,
            text=f"text{i}",
            status=KeywordStatus.UNSELECT.value,
            timestamp=round(time.time())
        ) for i in range(0, 20, 2)],
        status=StatusChoice.SAVE
    )


@pytest.fixture
def user_fixture() -> User:
    user = User.objects.create_user('fixture_user')
    return user


@pytest.fixture
def note_request_dto_fixture() -> NoteReqDto:
    return NoteReqDto(
        name='note_request_dto_fixture',
        status=StatusChoice.SAVE
    )


@pytest.fixture
def keyword_entities_fixture() -> List[KeywordEntity]:
    return [KeywordEntity(
        id=i+1,
        noteId=i+1,
        posX=i * 10,
        posY=i * 10,
        text=f"text{i}",
        status=KeywordStatus.UNSELECT.value,
        timestamp=str(round(time.time()))
    ) for i in range(10)]


@pytest.fixture
def note_summary_entity_fixture() -> NoteSummaryEntity:
    return NoteSummaryEntity(
        displayId=uuid.uuid4(),
        name='note1'
    )


def set_credential(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')


@pytest.fixture
def auth_client_fixture() -> Tuple[APIClient, User, set_credential]:
    client = APIClient()
    user = User.objects.create_user('fixture_user')
    set_credential(client, user.token)

    return (client, user, set_credential)


@pytest.fixture(scope='session')
def note_factory_fixture() -> NoteFactory:
    return NoteFactory()
