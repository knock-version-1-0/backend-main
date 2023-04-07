from typing import List

from pydantic import BaseModel


class KeywordResDto(BaseModel):
    order: int


class NoteResDto(BaseModel):
    displayId: str
    authorId: int
    name: str
    keywords: List[KeywordResDto]
    status: int
