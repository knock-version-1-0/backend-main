from typing import List, Optional

from pydantic import BaseModel

from core.utils.pydantic import RequestBody


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


class KeywordReqDto(RequestBody, BaseModel):
    posId: int


class NoteReqDto(RequestBody, BaseModel):
    name: str
    keywords: List[KeywordReqDto]=[]
    status: int
