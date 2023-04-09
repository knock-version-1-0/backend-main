import pytest
from mixer.backend.django import mixer
from django.db.utils import IntegrityError

from tests.fixtures import (
    user_fixture,
)
from core.repository import BaseRepository
from domains.exceptions import (
    AuthorizeNotCalledError,
    UserInvalidError,
    NoteDoesNotExistError,
)
from apps.notes.models import (
    Note,
    Keyword,
)
from core.models import StatusChoice
from di.notes_factory import NoteFactory


@pytest.mark.django_db
def test_is_user_authorized():
    """
    Call user from repository after authorize method is called
    """
    user = mixer.blend('users.User')

    repo = BaseRepository()
    with pytest.raises(AuthorizeNotCalledError.error_type):
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
    with pytest.raises(UserInvalidError):
        repo.authorize(user_id)
    
    with pytest.raises(UserInvalidError):
        repo.authorize(2)


@pytest.mark.django_db
def test_note_name_integrity():
    """
    UniqueConstraint -> posId, note
    """
    user = mixer.blend('users.User')
    Note.objects.create(
        author=user,
        keywords=[],
        status=StatusChoice.SAVE,
        name='note1'
    )

    with pytest.raises(IntegrityError):
        Note.objects.create(
            author=user,
            keywords=[],
            status=StatusChoice.SAVE,
            name='note1'
        )
    
    Note.objects.create(
        author=user,
        keywords=[],
        status=StatusChoice.SAVE,
        name='note2'
    )

    user = mixer.blend('users.User')
    Note.objects.create(
        author=user,
        keywords=[],
        status=StatusChoice.SAVE,
        name='note2'
    )


@pytest.mark.django_db(transaction=True)
def test_keyword_pos_id_integrity():
    """
    UniqueConstraint -> author, name
    """
    user = mixer.blend('users.User')
    note = Note.objects.create(
        author=user,
        keywords=[],
        status=StatusChoice.SAVE,
        name='note1'
    )

    with pytest.raises(IntegrityError):
        for _ in range(4):
            Keyword.objects.create(note=note, pos_id=1)

    note = Note.objects.create(
        author=user,
        keywords=[],
        status=StatusChoice.SAVE,
        name='note2'
    )
    for i in range(4):
        Keyword.objects.create(note=note, pos_id=i)


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

    with pytest.raises(NoteDoesNotExistError.error_type):
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

    with pytest.raises(NoteDoesNotExistError.error_type):
        repo.find_by_name(note.name)
    repo.find_by_name(note1.name)
