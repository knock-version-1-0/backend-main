from core.service import BaseService
from core.utils.data import ApiPayload
from adapters.dto.notes_dto import (
    NoteDto,
    KeywordDto,
)


class NoteService(BaseService):
    dto_class = NoteDto


class KeywordService(BaseService):
    dto_class = KeywordDto
    
    def create(self, data: dict, success='CREATE', **variables):
        return super().create(data=data, success=success, **variables)

    def update(self, key: object, data: dict, success='UPDATE', **variables):
        return super().update(key, data, success, **variables)

    def delete(self, key: object, success='DELETE', **variables):
        return super().delete(key, success, **variables)
