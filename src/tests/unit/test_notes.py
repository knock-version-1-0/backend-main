from typing import List

import pytest

from tests.fixtures import (
    note_entity_fixture
)
from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity,
)


@pytest.mark.unit
def test_note_entity_consistency(note_entity_fixture):
    """
    ```yaml
    Note:
        authorId: integer
        displayId: string
        name: string
        keywords: Keyword[]
        status: integer
    ```
    """

    assert isinstance(note_entity_fixture, NoteEntity)

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
        noteId: integer
        posId: integer
    ```
    """
    keywords: List[KeywordEntity] = note_entity_fixture.keywords

    for keyword in keywords:
        assert isinstance(keyword.noteId, int)
        assert isinstance(keyword.posId, int)
