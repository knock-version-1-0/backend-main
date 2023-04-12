from typing import List
import uuid

from pydantic import BaseModel, validator


class KeywordEntity(BaseModel):
    noteId: int
    posId: int
    text: str


class NoteEntity(BaseModel):
    id: int
    displayId: str
    authorId: int
    name: str
    keywords: List[KeywordEntity] = []
    status: int

    @validator('displayId', pre=True)
    def uuid_to_str(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
