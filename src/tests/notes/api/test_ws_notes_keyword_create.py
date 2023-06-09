import pytest

from rest_framework import status

from di.notes_factory import KeywordFactory
from domains.entities.notes_entity import KeywordEntity
from tests.factories.notes import make_notes, make_keyword_dto
from tests.factories.users import make_users
from core.utils.exceptions import get_error_name
from apps.notes.exceptions import NoteDoesNotExistError


@pytest.mark.django_db
def test_200_OK():
    user = make_users(size=1)[0]
    note = make_notes(author_id=user.id, size=1)[0]
    note_id = note.id

    dto = make_keyword_dto(note_id)

    service = KeywordFactory().service
    payload, status_code = service.create(dto.query_dict())
    
    assert payload.data == KeywordEntity(
        id=payload.data['id'],
        noteId=note.id,
        posX=dto.posX,
        posY=dto.posY,
        text=dto.text,
        parentId=dto.parentId,
        status=dto.status,
        timestamp=dto.timestamp
    ).dict()
    assert status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_404_NoteDoesNotExistError():
    dto = make_keyword_dto(note_id=1)

    service = KeywordFactory().service
    payload, status_code = service.create(dto.query_dict())
    
    assert payload.type == get_error_name(NoteDoesNotExistError())
    assert status_code == status.HTTP_404_NOT_FOUND
