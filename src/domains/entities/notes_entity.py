from typing import List

from pydantic import BaseModel


class NoteEntity(BaseModel):
    author_id: int
    display_id: str
    name: str
    keywords: List['KeywordEntity'] = []
    status: int


class KeywordEntity(BaseModel):
    note_id: int
    positions: List['KeywordPositionEntity'] = []


class KeywordPositionEntity(BaseModel):
    keyword_id: int
    order: int
