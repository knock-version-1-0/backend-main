from typing import List, Optional

from pydantic import BaseModel

from core.utils.pydantic import RequestBody


class KeywordReqDto(RequestBody, BaseModel):
    noteId: int
    posX: int
    posY: int
    text: str = ''
    parentId: Optional[int] = None
    status: int
    timestamp: int


class NoteReqDto(RequestBody, BaseModel):
    name: str
    status: int
