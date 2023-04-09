from typing import Optional

from core.repository import BaseRepository

from domains.entities.notes_entity import (
    NoteEntity
)


class NoteRepository(BaseRepository):
    def find_by_name(self, name: str) -> NoteEntity: ...
    def save(self, **kwargs) -> Optional[NoteEntity]: ...
