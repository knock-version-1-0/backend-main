from typing import List, Optional

from pydantic import BaseModel


class KeywordDto(BaseModel):
    noteId: Optional[int]
    posId: int


class NoteDto(BaseModel):
    id: int
    authorId: int
    displayId: str
    name: str
    keywords: List[KeywordDto]=[]
    status: int


class NoteReqDto(BaseModel):
    displayId: Optional[str]
    name: Optional[str]
    keywords: List[KeywordDto]=[]
    status: Optional[int]
