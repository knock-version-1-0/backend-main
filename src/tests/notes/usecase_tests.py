import pytest
import uuid
from mixer.backend.django import mixer
from unittest.mock import Mock

from tests.fixtures.users import (
    user_fixture,
)
from tests.fixtures.notes import (
    note_entity_fixture
)
from tests.factories.notes import make_notes, create_note_name
from apps.notes.exceptions import (
    NoteDoesNotExistError,
    NoteNameIntegrityError
)
from core.models import StatusChoice
from di.notes_factory import NoteFactory
from adapters.dto.notes_dto import (
    NoteDto
)
from domains.constants import MAX_NOTE_LIST_LIMIT
from domains.entities.notes_entity import (
    NoteEntity,
    NoteSummaryEntity,
)
from apps.notes.models import Note


@pytest.mark.django_db(transaction=True)
def test_note_name_integrity():
    """
    UseCase(NOTE1): Note.name shouldn't be duplicated when User update or create as same author
    """
    user = mixer.blend('users.User')

    size = 5
    note_list = make_notes(user.id, size=size)

    factory = NoteFactory()
    repo = factory.repository
    repo.authorize(user_id=user.id)

    note = note_list[0]

    with pytest.raises(NoteNameIntegrityError):
        dto = NoteDto(
            name=note.name,
            status=StatusChoice.SAVE
        )
        repo.save(**dto.dict())
    
    dto = NoteDto(
        name=create_note_name(),
        status=StatusChoice.SAVE
    )
    repo.save(**dto.dict())
    
    # update
    repo.find_one(key=note_list[size-1].displayId)

    with pytest.raises(NoteNameIntegrityError):
        dto = NoteDto(
            name=note.name
        )
        repo.save(**dto.dict())
    
    dto = NoteDto(
        name=create_note_name(),
        status=StatusChoice.SAVE
    )
    repo.save(**dto.dict())


@pytest.mark.django_db
def test_note_exists():
    """
    UseCase(NOTE3): Note should be existed when User retrieve
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
    UseCase(NOTE4): User retrieve only if Note.status = SAVE
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


@pytest.mark.unit
def test_note_list_item(note_entity_fixture):
    """
    UseCase(NOTE6): Note list의 item은 NoteSummary입니다.
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
    UseCase(NOTE5): Note list max length is 12
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


@pytest.mark.django_db
def test_filter_name_like():
    """
    UseCase(NOTE7): Note list can search by name
    """
    size = 5
    author = mixer.blend('users.User')

    repository = NoteFactory().repository
    repository.authorize(author.id)

    for i in range(size):
        dto = NoteDto(
            name=f'name{i}note',
            status=StatusChoice.SAVE
        )
        repository.save(**dto.dict())

    assert len(repository.find_by_author({'name': 'name'})) == size
    assert len(repository.find_by_author({'name': '0'})) == 1


@pytest.mark.django_db
def test_note_list_max_length():
    """
    UseCase(NOTE5): Note list max length is 12
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
    UseCase(NOTE8): Note list is ordered by created recently
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
