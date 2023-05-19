import logging
from typing import Optional
from rest_framework.request import QueryDict

from core.utils.decorators import authorize_required
from core.usecase import BaseUsecase

from domains.interfaces.notes_repository import (
    NoteRepository
)
from domains.constants import MAX_NOTE_LIST_LIMIT
from adapters.dto.notes_dto import NoteDto

logger = logging.getLogger(__name__)

__all__ = [
    'NoteUsecase',
]


class NoteUsecase(BaseUsecase):

    def __init__(self, repository: NoteRepository):
        self.repository = repository

    @authorize_required
    def list(self, params: Optional[QueryDict]=None, user_id: Optional[int]=None):
        params = params or QueryDict({})
        entities = self.repository.find_by_author(lookup={
            'name': params.get('name', ''),
            'offset': int(params.get('offset', 0)),
            'limit': int(params.get('limit', MAX_NOTE_LIST_LIMIT))
        })
        
        return [entity.literal() for entity in entities]

    @authorize_required
    def retrieve(self, key: str, user_id: int):
        entity = self.repository.find_one(key=key)

        return entity.literal()

    @authorize_required
    def create(self, data: NoteDto, user_id: int):
        entity = self.repository.save(
            name=data.name,
            status=data.status
        )

        return entity.literal()

    @authorize_required
    def update(self, key: str, data: NoteDto, user_id: int):
        self.repository.find_one(key=key)
        entity = self.repository.save(**data.dict())

        return entity.literal()

    @authorize_required
    def delete(self, key: str, user_id: int):
        self.repository.find_one(key=key)
        self.repository.delete()
