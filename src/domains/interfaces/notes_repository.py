from typing import Optional

from core.repository import BaseRepository

from domains.entities.notes_entity import (
    NoteEntity
)


class NoteRepository(BaseRepository):
    def find_by_display_id(self, display_id: str) -> NoteEntity: ...
    def save(self, **kwargs) -> Optional[NoteEntity]: ...
