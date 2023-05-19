from enum import Enum
from typing import List, Optional
import uuid
from pydantic import BaseModel, validator

from apps.notes.exceptions import NoteNameLengthLimitError
from domains.constants import NOTE_NAME_LENGTH_LIMIT
from core.entity import BaseEntity


class KeywordStatus(Enum):
    UNSELECT = 1
    READ = 2
    EDIT = 3


class KeywordEntity(BaseEntity):
    id: int
    noteId: int
    posX: int
    posY: int
    text: str
    parentId: Optional[int] = None
    status: int
    timestamp: int


class NoteEntity(BaseEntity):
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
    
    @validator('name', pre=True)
    def check_name_length_limit(cls, v):
        if len(v) > NOTE_NAME_LENGTH_LIMIT:
            raise NoteNameLengthLimitError(NOTE_NAME_LENGTH_LIMIT)
        return v


class NoteSummaryEntity(BaseEntity):
    displayId: str
    name: str

    @validator('displayId', pre=True)
    def uuid_to_str(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
