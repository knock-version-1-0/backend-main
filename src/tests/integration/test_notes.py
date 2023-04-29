import pytest
from mixer.backend.django import mixer
from django.db.utils import IntegrityError

from tests.fixtures import (
    user_fixture,
)
from core.repository import BaseRepository
from core.exceptions import (
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
    assert repo.user == None

    repo.authorize(user.pk)
    assert bool(repo.user)


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


@pytest.mark.django_db(transaction=True)
def test_note_name_integrity():
    """
    UniqueConstraint -> posId, note
    """
    user = mixer.blend('users.User')
    Note.objects.create(
        author=user,
        status=StatusChoice.SAVE,
        name='note1'
    )

    with pytest.raises(IntegrityError):
        Note.objects.create(
            author=user,
            status=StatusChoice.SAVE,
            name='note1'
        )
    
    Note.objects.create(
        author=user,
        status=StatusChoice.SAVE,
        name='note2'
    )

    user = mixer.blend('users.User')
    Note.objects.create(
        author=user,
        status=StatusChoice.SAVE,
        name='note2'
    )


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

    with pytest.raises(NoteDoesNotExistError):
        repo.find_one(key=2)
    repo.find_one(note1.display_id)


@pytest.mark.django_db
def test_note_saved():
    """
    Note.status = SAVE일 때만 User가 조회할 수 있습니다.
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

    with pytest.raises(NoteDoesNotExistError):
        repo.find_one(note.display_id)
    repo.find_one(note1.display_id)

    assert len(repo.find_by_author()) == 1


@pytest.mark.django_db
def test_find_by_author():
    """
    Author의 Note만 list를 조회할 수 있습니다.
    """
    author = mixer.blend('users.User')
    other = mixer.blend('users.User')

    note = mixer.blend('notes.Note',
                        author=author,
                        name='note',
                        status=StatusChoice.SAVE)
    note1 = mixer.blend('notes.Note',
                       author=other,
                       name='note1',
                       status=StatusChoice.SAVE)

    repository = NoteFactory().repository
    repository.authorize(author.id)

    result = repository.find_by_author()
    assert len(result) == 1
    assert result[0].name == note.name


@pytest.mark.django_db
def test_filter_name_like():
    """
    Note list는 name별로 search 가능합니다.
    """
    size = 5
    author = mixer.blend('users.User')
    notes = [Note.objects.create(
        author=author,
        name=f'name{i}note',
        status=StatusChoice.SAVE
    ) for i in range(size)]
    assert len(Note.objects.filter(name__contains='')) == size
    assert len(Note.objects.filter(name__contains='1')) == 1

    repository = NoteFactory().repository
    repository.authorize(author.id)

    assert len(repository.find_by_author({'name': 'name'})) == size
    assert len(repository.find_by_author({'name': '0'})) == 1
