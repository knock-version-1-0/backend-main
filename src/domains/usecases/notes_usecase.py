import logging
from typing import Optional

from core.utils.decorators import authorize_required
from core.usecase import BaseUsecase

from domains.interfaces.notes_repository import (
    NoteRepository
)
from domains.constants import MAX_NOTE_LIST_LIMIT
from adapters.dto.notes_dto import NoteReqDto

logger = logging.getLogger(__name__)

__all__ = [
    'NoteUsecase',
]


class NoteUsecase(BaseUsecase):

    def __init__(self, repository: NoteRepository, context: Optional[dict]=None):
        self.repository = repository

    @authorize_required
    def list(self, params=None, user_id: Optional[int]=None):
        params = params or {}
        entities = self.repository.find_by_author(lookup={
            'name': params.get('name', ''),
            'offset': int(params.get('offset', 0)),
            'limit': int(params.get('limit', MAX_NOTE_LIST_LIMIT))
        })
        
        return [entity.dict() for entity in entities]

    @authorize_required
    def retrieve(self, key: str, user_id: int):
        entity = self.repository.find_one(key=key)

        return entity.dict()

    @authorize_required
    def create(self, req_body: NoteReqDto, user_id: int):
        entity = self.repository.save(
            name=req_body.name,
            status=req_body.status
        )

        return entity.dict()

    @authorize_required
    def update(self, key: str, req_body: NoteReqDto, user_id: int) -> dict:
        self.repository.find_one(key=key)
        entity = self.repository.save(**req_body.dict())

        return entity.dict()

    @authorize_required
    def delete(self, key: str, user_id: int):
        self.repository.find_one(key=key)
        self.repository.delete()
