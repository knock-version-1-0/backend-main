import uuid

from typing import List

import pytest
from unittest.mock import Mock

from tests.fixtures.notes import (
    note_entity_fixture,
    keyword_entities_fixture,
    note_summary_entity_fixture
)
from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity,
    NoteSummaryEntity,
)
from domains.usecases.notes_usecase import (
    NoteUsecase,
)
from core.exceptions import (
    NoteNameIntegrityError,
    NoteNameLengthLimitError
)
from di.notes_factory import (
    NoteFactory,
)
from apps.notes.models import Note
from core.models import StatusChoice
from domains.constants import MAX_NOTE_LIST_LIMIT, NOTE_NAME_LENGTH_LIMIT


@pytest.mark.unit
def test_note_list_item(note_entity_fixture):
    """
    Note list의 item은 NoteSummary입니다.
    """
    queryset = Mock()
    queryset.filter.return_value = [Note(
        display_id=note_entity_fixture.displayId,
        name=note_entity_fixture.name,
        status=note_entity_fixture.status,
        id=note_entity_fixture.id
    )]
    repository = NoteFactory().repository
    repository.queryset = queryset

    entities = repository.find_by_author()
    assert not isinstance(entities[0], NoteEntity)
    assert isinstance(entities[0], NoteSummaryEntity)


@pytest.mark.unit
def test_note_list_limit():
    """
    Note list는 한번에 12개 까지 조회 가능합니다.
    """
    queryset = Mock()
    queryset.filter.return_value = [Note(
        id=i+1,
        display_id=uuid.uuid4(),
        name=f'name{i}',
        status=StatusChoice.SAVE,
    ) for i in range(30)]

    repository = NoteFactory().repository
    repository.queryset = queryset

    entities = repository.find_by_author({
        'offset': 0,
        'limit': 5
    })
    assert len(entities) == 5
    
    # limit이 MAX_NOTE_LIST_LIMIT을 초과할 경우
    entities = repository.find_by_author({
        'offset': 0,
        'limit': MAX_NOTE_LIST_LIMIT + 1
    })
    assert len(entities) == MAX_NOTE_LIST_LIMIT

    entities = repository.find_by_author({
        'offset': 0
    })
    assert len(entities) == MAX_NOTE_LIST_LIMIT


@pytest.mark.unit
def test_note_name_length_limit():
    """
    Note name의 length는 25를 초과할 수 없습니다.
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
