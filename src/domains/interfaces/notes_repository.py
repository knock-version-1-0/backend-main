from typing import Optional, List, Type, TypedDict

from core.repository import BaseRepository

from domains.entities.notes_entity import (
    NoteEntity,
    NoteSummaryEntity,
    KeywordEntity
)


NoteRepositoryContext = TypedDict('NoteRepositoryContext', {
    'NoteEntity': Type[NoteEntity],
    'KeywordEntity': Type[KeywordEntity],
    'NoteSummaryEntity': Type[NoteSummaryEntity]
})


class NoteRepository(BaseRepository):
    def __init__(self, context: NoteRepositoryContext): ...
    def find_one(self, key: str) -> NoteEntity: ...
    def find_by_author(self, lookup: dict={}) -> List[NoteSummaryEntity]: ...
    def save(self, **kwargs) -> NoteEntity: ...
    def delete(self) -> None: ...


KeywordRepositoryContext = TypedDict('KeywordRepositoryContext', {
    'KeywordEntity': Type[KeywordEntity]
})


class KeywordRepository(BaseRepository):
    def __init__(self, context: KeywordRepositoryContext): ...
    def save(self, **kwargs) -> KeywordEntity: ...
