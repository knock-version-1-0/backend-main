import uuid
import pytest

from mixer.backend.django import mixer
from tests.fixtures import (
    user_fixture,
)

from apps.notes.models import (
    Note,
    Keyword,
)
from core.models import StatusChoice
from core.repository import BaseRepository
from domains.exceptions import (
    NoteNameIntegrityError,
    KeywordPosIdIntegrityError,
    NoteDoesNotExistError,
    AuthorizeNotCalledError,
    RepositoryAuthorizeError
)
from adapters.dto.notes_dto import (
    NoteReqDto,
    KeywordBaseDto
)
from di.notes_factory import NoteFactory


@pytest.mark.django_db(transaction=True)
def test_note_name_integrity():
    """
    동일한 Author일 경우 Note.name을 중복해서 등록할 수 없습니다.
    """
    user = mixer.blend('users.User')
    usecase = NoteFactory().usecase
    keyword_size = 16

    create_note = lambda name, user: usecase.create(NoteReqDto(
        displayId=str(uuid.uuid4()),
        name=name,
        keywords=[KeywordBaseDto(posId=i) for i in range(keyword_size)],
        status=StatusChoice.SAVE
    ), user_id=user.pk)

    name = 'name'
    create_note(name, user)

    with pytest.raises(NoteNameIntegrityError):
        create_note(name, user)
    
    create_note('name1', user)

    user = mixer.blend('users.User')
    create_note(name, user)


@pytest.mark.django_db(transaction=True)
def test_keyword_pos_id_integrity():
    """
    Keyword.posId는 Note내에서 중복을 허용하지 않습니다.
    """
    usecase = NoteFactory().usecase
    user = mixer.blend('users.User')

    create_note = lambda name, keywords: usecase.create(NoteReqDto(
        displayId=str(uuid.uuid4()),
        name=name,
        keywords=keywords,
        status=StatusChoice.SAVE
    ), user_id=user.pk)

    keywords = [KeywordBaseDto(posId=1) for _ in range(4)]
    with pytest.raises(KeywordPosIdIntegrityError):
        create_note('name1', keywords)
    
    keywords = [KeywordBaseDto(posId=i) for i in range(4)]
    create_note('name2', keywords)


@pytest.mark.django_db
def test_keyword_order_by():
    """
    Keyword는 Keyword.posId 별로 정렬됩니다.
    """
    note = mixer.blend('notes.Note')

    for i in range(9, -1, -1):
        Keyword.objects.create(
            note=note,
            pos_id=i
        )
    
    keywords = Keyword.objects.filter(note=note)
    for i in range(10):
        assert keywords[i].pos_id == i


@pytest.mark.django_db
def test_note_exists():
    """
    Note가 존재할 경우만 Note를 조회할 수 있습니다.
    """
    user = mixer.blend('users.User')
    note1 = mixer.blend('notes.Note',
                       author=user,
                       name='note1',
                       status=StatusChoice.SAVE)

    factory = NoteFactory()
    repo = factory.repository
    repo.authorize(user.pk)

    with pytest.raises(NoteDoesNotExistError.type):
        repo.find_by_name('note')
    repo.find_by_name(note1.name)


@pytest.mark.django_db
def test_note_saved():
    """
    Note.status = SAVE일 때만 조회할 수 있습니다.
    """
    user = mixer.blend('users.User')
    note = mixer.blend('notes.Note',
                        author=user,
                        name='note',
                        status=StatusChoice.DELETE)
    note1 = mixer.blend('notes.Note',
                       author=user,
                       name='note1',
                       status=StatusChoice.SAVE)
    
    factory = NoteFactory()
    repo = factory.repository
    repo.authorize(user.pk)

    with pytest.raises(NoteDoesNotExistError.type):
        repo.find_by_name(note.name)
    repo.find_by_name(note1.name)


@pytest.mark.django_db
def test_is_user_authorized():
    """
    Call user from repository after authorize method is called
    """
    user = mixer.blend('users.User')

    repo = BaseRepository()
    with pytest.raises(AuthorizeNotCalledError.type):
        repo.user

    repo.authorize(user.pk)
    repo.user


@pytest.mark.django_db
def test_repository_authorize(user_fixture):
    """
    Repository authorize method test
    """
    user_id = user_fixture.id
    repo = BaseRepository()
    repo.authorize(user_id)

    user_fixture.is_active = False
    user_fixture.save()
    with pytest.raises(RepositoryAuthorizeError):
        repo.authorize(user_id)
    
    with pytest.raises(RepositoryAuthorizeError):
        repo.authorize(2)
