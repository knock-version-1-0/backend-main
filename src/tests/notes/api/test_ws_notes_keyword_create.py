import pytest

from di.notes_factory import KeywordFactory
from domains.entities.notes_entity import KeywordEntity
from tests.factories.notes import make_notes, make_keyword_dto
from tests.factories.users import make_users
from tests.utils import ws_response
from core.utils.exceptions import get_error_name
from apps.notes.exceptions import NoteDoesNotExistError
from apps.users.exceptions import (
    UserInvalidError,
    UserPermissionError
)
from apps.notes.consumers import NoteCreateKeywordConsumer
from core.utils.data import ApiPayload, ErrorDetail


@pytest.mark.django_db
def test_200_OK():
    user = make_users(size=1)[0]
    note = make_notes(author_id=user.id, size=1)[0]
    dto = make_keyword_dto(note_id=note.id)

    response = ws_response(
        consumer=NoteCreateKeywordConsumer(KeywordFactory()),
        data=dto.query_dict(),
        token=user.accessToken.value
    )
    payload = ApiPayload(**response.data)
    
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
    assert payload.status == 'OK'


@pytest.mark.django_db
def test_401_UserInvalidError():
    user = make_users(size=1)[0]
    note = make_notes(author_id=user.id, size=1)[0]
    dto = make_keyword_dto(note_id=note.id)

    response = ws_response(
        consumer=NoteCreateKeywordConsumer(KeywordFactory()),
        data=dto.query_dict(),
        token=user.accessToken.value + '_'
    )
    error_detail = ErrorDetail(**response.data)

    assert error_detail.type == get_error_name(UserInvalidError())


@pytest.mark.django_db
def test_403_UserPermissionError():
    users = make_users(size=2)
    note = make_notes(author_id=users[0].id, size=1)[0]
    dto = make_keyword_dto(note_id=note.id)

    response = ws_response(
        consumer=NoteCreateKeywordConsumer(KeywordFactory()),
        data=dto.query_dict(),
        token=users[1].accessToken.value
    )
    error_detail = ErrorDetail(**response.data)

    assert error_detail.type == get_error_name(UserPermissionError())


@pytest.mark.django_db
def test_404_NoteDoesNotExistError():
    user = make_users(size=1)[0]
    note = make_notes(author_id=user.id, size=1)[0]
    dto = make_keyword_dto(note_id=note.id + 1)

    response = ws_response(
        consumer=NoteCreateKeywordConsumer(KeywordFactory()),
        data=dto.query_dict(),
        token=user.accessToken.value
    )
    error_detail = ErrorDetail(**response.data)
    
    assert error_detail.type == get_error_name(NoteDoesNotExistError())
