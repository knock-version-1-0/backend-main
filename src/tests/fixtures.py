from typing import List
import random, uuid

import pytest

from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity
)
from core.models import StatusChoice


@pytest.fixture
def note_entity_fixture() -> NoteEntity:
    return NoteEntity(
        id=1,
        authorId=1,
        displayId=uuid.uuid4(),
        name='note1',
        keywords=[KeywordEntity(
            noteId=1,
            posId=i
        ) for i in range(0, 20, 2)],
        status=StatusChoice.SAVE
    )