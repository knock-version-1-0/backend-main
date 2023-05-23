import time
from typing import List
import uuid
import pytest
import datetime

from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity,
    NoteSummaryEntity
)
from core.models import StatusChoice
from domains.entities.notes_entity import KeywordStatus
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
        status=StatusChoice.SAVE,
        createdAt=datetime.datetime.now(),
        updatedAt=datetime.datetime.now()
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
        name='note1',
        createdAt=datetime.datetime.now(),
        updatedAt=datetime.datetime.now()
    )


@pytest.fixture(scope='session')
def note_factory_fixture() -> NoteFactory:
    return NoteFactory()
