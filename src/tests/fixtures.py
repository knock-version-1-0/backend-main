from typing import List
import random, uuid

import pytest

from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity,
    NoteSummaryEntity
)
from adapters.dto.notes_dto import (
    NoteReqDto,
    KeywordReqDto,
    NoteDto,
    KeywordDto,
    NoteSummaryDto
)
from core.models import StatusChoice
from apps.users.models import User


@pytest.fixture
def note_entity_fixture() -> NoteEntity:
    return NoteEntity(
        id=1,
        authorId=1,
        displayId=uuid.uuid4(),
        name='note1',
        keywords=[KeywordEntity(
            noteId=1,
            posId=i,
            text='text'
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
        keywords=[KeywordReqDto(posId=i, text=f'text{i}') for i in range(10)],
        status=StatusChoice.SAVE
    )


@pytest.fixture
def note_usecase_context_fixture() -> dict:
    return {
        'NoteDto': NoteDto,
        'KeywordDto': KeywordDto,
        'NoteSummaryDto': NoteSummaryDto
    }


@pytest.fixture
def keyword_entities_fixture() -> List[KeywordEntity]:
    return [KeywordEntity(
        noteId=1,
        posId=i,
        text=f'text{i}'
    ) for i in range(10)]


@pytest.fixture
def note_summary_entity_fixture() -> NoteSummaryEntity:
    return NoteSummaryEntity(
        displayId=uuid.uuid4(),
        name='note1'
    )
