import pytest

from di.notes_factory import KeywordFactory
from tests.factories.notes import make_notes, make_keyword_dto
from tests.factories.users import make_users
from tests.utils import ws_response
from core.utils.exceptions import get_error_name
from apps.notes.exceptions import (
    KeywordDoesNotExistError
)
from apps.users.exceptions import (
    UserInvalidError,
    UserPermissionError
)
from apps.notes.consumers import NoteKeywordConsumer
from core.utils.data import ApiPayload, ErrorDetail



@pytest.mark.django_db
def test_DELETE():
    user = make_users(size=1)[0]
    note = make_notes(author_id=user.id, size=1)[0]
    dto = make_keyword_dto(note_id=note.id)

    repository = KeywordFactory().repository
    repository.authorize(user.id)
    keyword_entity = repository.save(**dto.dict())

    response = ws_response(
        consumer=NoteKeywordConsumer(KeywordFactory()),
        method='delete',
        data=None,
        token=user.accessToken.value,
        key=keyword_entity.id
    )
    payload = ApiPayload(**response.data)

    assert payload.status == 'DELETE'


@pytest.mark.django_db
def test_UserInvalidError():
    user = make_users(size=1)[0]
    note = make_notes(author_id=user.id, size=1)[0]
    dto = make_keyword_dto(note_id=note.id)

    repository = KeywordFactory().repository
    repository.authorize(user.id)
    keyword_entity = repository.save(**dto.dict())

    response = ws_response(
        consumer=NoteKeywordConsumer(KeywordFactory()),
        method='delete',
        data=None,
        token=user.accessToken.value + '_',
        key=keyword_entity.id
    )

    error_detail = ErrorDetail(**response.data)

    assert error_detail.type == get_error_name(UserInvalidError())


@pytest.mark.django_db
def test_UserPermissionError():
    users = make_users(size=2)
    note = make_notes(author_id=users[0].id, size=1)[0]
    dto = make_keyword_dto(note_id=note.id)

    repository = KeywordFactory().repository
    repository.authorize(users[0].id)
    keyword_entity = repository.save(**dto.dict())

    response = ws_response(
        consumer=NoteKeywordConsumer(KeywordFactory()),
        method='delete',
        data=None,
        token=users[1].accessToken.value,
        key=keyword_entity.id
    )

    error_detail = ErrorDetail(**response.data)

    assert error_detail.type == get_error_name(UserPermissionError())


@pytest.mark.django_db
def test_KeywordDoesNotExistError():
    user = make_users(size=1)[0]
    note = make_notes(author_id=user.id, size=1)[0]
    dto = make_keyword_dto(note_id=note.id)

    repository = KeywordFactory().repository
    repository.authorize(user.id)
    keyword_entity = repository.save(**dto.dict())

    response = ws_response(
        consumer=NoteKeywordConsumer(KeywordFactory()),
        method='delete',
        data=None,
        token=user.accessToken.value,
        key=keyword_entity.id + 1
    )

    error_detail = ErrorDetail(**response.data)

    assert error_detail.type == get_error_name(KeywordDoesNotExistError())
