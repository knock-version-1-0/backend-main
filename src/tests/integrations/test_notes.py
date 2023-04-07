import pytest

from mixer.backend.django import mixer

from apps.notes.models import (
    Note,
    Keyword,
)
from core.models import StatusChoice
from domains.entities.exceptions import (
    NoteNameIntegrityError,
    KeywordPositionOrderIntegrityError,
    NoteDoesNotExistError,
    RepositoryAuthorizeError
)
from di.notes_factory import NoteFactory


@pytest.mark.django_db(transaction=True)
def test_note_name_integrity():
    """
    동일한 Author일 경우 Note.name을 중복해서 등록할 수 없습니다.
    """
    author = mixer.blend('users.User')
    name = 'Test Note'
    note1 = Note.objects.create(author=author, name=name)
    
    # Test that creating a note with the same name and author raises an IntegrityError
    with pytest.raises(NoteNameIntegrityError.type):
        note2 = Note.objects.create(author=author, name=name)

    # Test that creating a note with a different name and the same author does not raise an error
    note3 = Note.objects.create(author=author, name='Another Note')

    # Test that creating a note with the same name but a different author does not raise an error
    author2 = mixer.blend('users.User')
    note4 = Note.objects.create(author=author2, name=name)


@pytest.mark.django_db(transaction=True)
def test_keyword_order_integrity():
    """
    Keyword.order는 Note내에서 중복을 허용하지 않습니다.
    """
    note1 = mixer.blend('notes.Note')
    note2 = mixer.blend('notes.Note')

    obj = Keyword.objects.create(note=note1, order=1)

    with pytest.raises(KeywordPositionOrderIntegrityError.type):
        obj = Keyword.objects.create(note=note1, order=1)

    obj = Keyword.objects.create(note=note2, order=1)


@pytest.mark.django_db
def test_keyword_order_by():
    """
    Keyword는 Keyword.order 별로 정렬됩니다.
    """
    note = mixer.blend('notes.Note')

    for i in range(10, 0, -1):
        Keyword.objects.create(
            note=note,
            order=i
        )
    
    keywords = Keyword.objects.filter(note=note)
    for i in range(10):
        assert keywords[i].order == i+1


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
    Note는 User만 조회할 수 있습니다.
    """
    user = mixer.blend('users.User')
    note = mixer.blend('notes.Note',
                       author=user,
                       name='note1',
                       status=StatusChoice.SAVE)

    factory = NoteFactory()
    repo = factory.repository
    with pytest.raises(RepositoryAuthorizeError.type):
        repo.find_by_name(note.name)

    repo.authorize(user.pk)
    repo.find_by_name(note.name)
