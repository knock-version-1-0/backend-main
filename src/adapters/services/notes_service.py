from core.service import BaseService
from adapters.dto.notes_dto import (
    NoteDto,
    KeywordDto,
)


class NoteService(BaseService):
    dto_class = NoteDto


class KeywordService(BaseService):
    dto_class = KeywordDto
    
    def create(self, data: dict, success='OK',**variables):
        return super().create(data=data, success=success, **variables)
