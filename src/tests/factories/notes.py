from typing import List
import faker

from core.models import StatusChoice
from domains.constants import NOTE_NAME_LENGTH_LIMIT
from domains.entities.notes_entity import (
    NoteEntity,
    NoteSummaryEntity,
    KeywordEntity
)
from apps.notes.models import KeywordStatusChoice
from adapters.dto.notes_dto import KeywordDto
from di.notes_factory import NoteFactory
from tests.factories.utils import timestamp

fake = faker.Faker()


def create_note_name() -> str:
    return fake.unique.name()[:NOTE_NAME_LENGTH_LIMIT] if len(fake.unique.name()) > NOTE_NAME_LENGTH_LIMIT else fake.unique.name()


def make_notes(author_id: int, size=5) -> List[NoteEntity]:
    repository = NoteFactory().repository
    repository.authorize(user_id=author_id)

    notes = []
    for _ in range(size):
        notes.append(repository.save(
            name = create_note_name(),
            status = StatusChoice.SAVE
        ))
    
    return notes


def make_keyword_dto(note_id: int) -> KeywordDto:
    return KeywordDto(
        noteId=note_id,
        posX=0,
        posY=0,
        text='',
        parentId=None,
        status=KeywordStatusChoice.UNSELECT,
        timestamp=timestamp
    )
