from typing import List, Optional

from pydantic import BaseModel


class KeywordBaseDto(BaseModel):
    posId: int


class NoteResDto(BaseModel):
    authorId: int
    displayId: str
    name: str
    keywords: List[KeywordBaseDto]=[]
    status: int


class NoteReqDto(BaseModel):
    displayId: Optional[str]
    name: Optional[str]
    keywords: List[KeywordBaseDto]=[]
    status: Optional[int]
