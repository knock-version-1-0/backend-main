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

    def dict(self) -> dict:
        return {
            'note_id': self.noteId,
            'pos_x': self.posX,
            'pos_y': self.posY,
            'text': self.text,
            'parent_id': self.parentId,
            'status': self.status,
            'timestamp': self.timestamp
        }


class NoteReqDto(RequestBody, BaseModel):
    name: str
    status: int

    def dict(self) -> dict:
        return {
            'name': self.name,
            'status': self.status
        }
