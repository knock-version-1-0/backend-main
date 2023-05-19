import pytest
import uuid
from typing import List

from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity
)
from tests.fixtures.notes import (
    note_entity_fixture,
    note_summary_entity_fixture
)
from apps.notes.exceptions import (
    NoteNameLengthLimitError
)
from domains.constants import NOTE_NAME_LENGTH_LIMIT


@pytest.mark.unit
def test_note_entity_consistency(note_entity_fixture):
    """
    ```yaml
    Note:
        id: integer
        authorId: integer
        displayId: string
        name: string
        keywords: Keyword[]
        status: integer
    ```
    """

    assert isinstance(note_entity_fixture, NoteEntity)

    assert isinstance(note_entity_fixture.id, int)
    assert isinstance(note_entity_fixture.authorId, int)
    assert isinstance(note_entity_fixture.displayId, str)
    assert isinstance(note_entity_fixture.name, str)
    assert bool(note_entity_fixture.keywords)
    assert isinstance(note_entity_fixture.keywords, list)
    assert isinstance(note_entity_fixture.status, int)


@pytest.mark.unit
def test_keyword_entity_consistency(note_entity_fixture):
    """
    ```yaml
    Keyword:
        id: integer
        noteId: integer
        posX: integer
        posY: integer
        text: string
        parentId: integer
        status: integer
            - 1: UNSELECT
            - 2: READ
            - 3: EDIT
        timestamp: integer
    ```
    """
    keywords: List[KeywordEntity] = note_entity_fixture.keywords

    for keyword in keywords:
        assert isinstance(keyword.id, int)
        assert isinstance(keyword.noteId, int)
        assert isinstance(keyword.posX, int)
        assert isinstance(keyword.posY, int)
        assert isinstance(keyword.text, str)
        assert isinstance(keyword.parentId, int) or keyword.parentId == None
        assert isinstance(keyword.status, int)
        assert isinstance(keyword.timestamp, int)


@pytest.mark.unit
def test_note_summary_consistency(note_summary_entity_fixture):
    """
    ```yaml
    NoteSummary:
        displayId: str
        name: str
    ```
    """
    summary = note_summary_entity_fixture
    
    assert isinstance(summary.displayId, str)
    assert isinstance(summary.name, str)


@pytest.mark.unit
def test_note_name_length_limit():
    """
    Entity(NOTE1): Note.name max_length == 25
    """
    note = NoteEntity(
        id=1,
        displayId=uuid.uuid4(),
        authorId=1,
        name='name',
        keywords=[],
        status=1
    )

    with pytest.raises(NoteNameLengthLimitError):
        note = NoteEntity(
            id=1,
            displayId=uuid.uuid4(),
            authorId=1,
            name='n' * (NOTE_NAME_LENGTH_LIMIT+1),
            keywords=[],
            status=1
        )
