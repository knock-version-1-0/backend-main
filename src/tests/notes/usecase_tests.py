import pytest
import uuid
from mixer.backend.django import mixer
from django.db.utils import IntegrityError

from tests.fixtures.users import (
    user_fixture,
)
from tests.factories.notes import make_notes, create_note_name
from core.exceptions import (
    UserInvalidError,
    NoteDoesNotExistError,
)
from core.models import StatusChoice
from di.notes_factory import NoteFactory
from adapters.dto.notes_dto import (
    NoteReqDto
)
from domains.constants import MAX_NOTE_LIST_LIMIT


@pytest.mark.django_db(transaction=True)
def test_note_name_integrity():
    """
    Note.name shouldn't be duplicated when User update or create as same author
    """
    user = mixer.blend('users.User')

    size = 5
    note_list = make_notes(user.id, size=size)

    factory = NoteFactory()
    repo = factory.repository
    repo.authorize(user_id=user.id)

    note = note_list[0]

    with pytest.raises(IntegrityError):
        dto = NoteReqDto(
            name=note.name,
            status=StatusChoice.SAVE
        )
        repo.save(**dto.dict())
    
    dto = NoteReqDto(
        name=create_note_name(),
        status=StatusChoice.SAVE
    )
    repo.save(**dto.dict())
    
    # update
    repo.find_one(key=note_list[size-1].displayId)

    with pytest.raises(IntegrityError):
        dto = NoteReqDto(
            name=note.name
        )
        repo.save(**dto.dict())
    
    dto = NoteReqDto(
        name=create_note_name(),
        status=StatusChoice.SAVE
    )
    repo.save(**dto.dict())


@pytest.mark.django_db
def test_note_exists():
    """
    Note should be existed when User retrieve
    """
    size = 10
    user = mixer.blend('users.User')
    note = make_notes(user.id, size=size)[0]

    factory = NoteFactory()
    repo = factory.repository
    repo.authorize(user.id)

    with pytest.raises(NoteDoesNotExistError):
        repo.find_one(key=str(uuid.uuid4()))
    repo.find_one(note.displayId)


@pytest.mark.django_db
def test_note_saved():
    """
    User retrieve only if Note.status = SAVE
    """
    user = mixer.blend('users.User')
    notes = make_notes(user.id, size=2)
    
    factory = NoteFactory()
    repo = factory.repository
    repo.authorize(user.pk)

    repo.find_one(notes[0].displayId)
    repo.save(status=StatusChoice.DELETE)

    with pytest.raises(NoteDoesNotExistError):
        repo.find_one(notes[0].displayId)
    repo.find_one(notes[1].displayId)


@pytest.mark.django_db
def test_filter_name_like():
    """
    Note list can search by name
    """
    size = 5
    author = mixer.blend('users.User')

    repository = NoteFactory().repository
    repository.authorize(author.id)

    for i in range(size):
        dto = NoteReqDto(
            name=f'name{i}note',
            status=StatusChoice.SAVE
        )
        repository.save(**dto.dict())

    assert len(repository.find_by_author({'name': 'name'})) == size
    assert len(repository.find_by_author({'name': '0'})) == 1


@pytest.mark.django_db
def test_note_list_max_length():
    """
    Note list max length is 12
    """
    assert MAX_NOTE_LIST_LIMIT == 12
    size = MAX_NOTE_LIST_LIMIT * 2

    author = mixer.blend('users.User')
    note_list = make_notes(author.id, size=size)

    repository = NoteFactory().repository
    repository.authorize(user_id=author.id)

    assert len(repository.find_by_author()) == MAX_NOTE_LIST_LIMIT


@pytest.mark.django_db
def test_order_by_created_desc():
    """
    Note list is ordered by created recently
    """
    author = mixer.blend('users.User')

    size = 10
    note_list = make_notes(author.id, size=size)

    repository = NoteFactory().repository
    repository.authorize(user_id=author.id)

    note_list = repository.find_by_author()
    current = size+1
    for item in note_list:
        current -= 1
        note = repository.find_one(item.displayId)
        assert current == note.id
