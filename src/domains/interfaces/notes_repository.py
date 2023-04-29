from typing import Optional, List

from core.repository import BaseRepository

from domains.entities.notes_entity import (
    NoteEntity,
    NoteSummaryEntity
)


class NoteRepository(BaseRepository):
    def find_one(self, key: str) -> NoteEntity: ...
    def find_by_author(self, lookup: dict={}) -> List[NoteSummaryEntity]: ...
    def save(self, **kwargs) -> Optional[NoteEntity]: ...
    def delete(self, key: str) -> None: ...
