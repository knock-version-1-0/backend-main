from typing import List

import pytest
from unittest.mock import Mock
from django.db.utils import IntegrityError

from tests.fixtures import (
    note_entity_fixture,
    note_request_dto_fixture,
    note_usecase_context_fixture,
    keyword_entities_fixture,
)
from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity,
)
from domains.usecases.notes_usecase import (
    NoteUsecase,
)
from domains.exceptions import (
    NoteNameIntegrityError,
    KeywordPosIdIntegrityError,
)
from di.notes_factory import (
    NoteFactory,
)


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
        noteId: integer
        posId: integer
    ```
    """
    keywords: List[KeywordEntity] = note_entity_fixture.keywords

    for keyword in keywords:
        assert isinstance(keyword.noteId, int)
        assert isinstance(keyword.posId, int)


@pytest.mark.unit
def test_note_name_duplicate(note_request_dto_fixture, note_usecase_context_fixture):
    """
    동일한 Author일 경우 Note.name을 중복해서 등록할 수 없습니다.

    - 중복될 경우 repository.save는 IntegrityError를 raise합니다.
    - usecase.create 호출 시 IntegrityError에 대해 NoteNameIntegrityError를 raise합니다.
    """
    repository = Mock()
    repository.save.side_effect = IntegrityError('Note')
    usecase = NoteUsecase(
        repository,
        note_usecase_context_fixture
    )
    with pytest.raises(NoteNameIntegrityError):
        usecase.create(note_request_dto_fixture, user_id=1)


@pytest.mark.unit
def test_keyword_pos_id_duplicate(note_request_dto_fixture, note_usecase_context_fixture):
    """
    Keyword.posId는 Note내에서 중복을 허용하지 않습니다.

    - 중복될 경우 repository.save는 IntegrityError를 raise합니다.
    - usecase.create 호출 시 IntegrityError에 대해 NoteNameIntegrityError를 raise합니다.
    """
    repository = Mock()
    repository.save.side_effect = IntegrityError('Keyword')
    usecase = NoteUsecase(
        repository,
        note_usecase_context_fixture
    )
    with pytest.raises(KeywordPosIdIntegrityError):
        usecase.create(note_request_dto_fixture, user_id=1)
