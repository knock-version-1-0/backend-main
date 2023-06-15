from typing import Optional
from rest_framework.request import QueryDict

from core.utils.decorators import authorize_required
from core.usecase import BaseUsecase
from core.utils.typing import LiteralData

from domains.interfaces.notes_repository import (
    NoteRepository,
    KeywordRepository
)
from domains.constants import MAX_NOTE_LIST_LIMIT
from adapters.dto.notes_dto import (
    NoteDto,
    KeywordDto
)


class NoteUsecase(BaseUsecase):

    def __init__(self, repository: NoteRepository):
        self.repository = repository

    @authorize_required
    def list(self, params: Optional[QueryDict]=None, **variables):
        params = params or QueryDict({})
        entities = self.repository.find_by_author(lookup={
            'name': params.get('name', ''),
            'offset': int(params.get('offset', 0)),
            'limit': int(params.get('limit', MAX_NOTE_LIST_LIMIT))
        })
        
        return [entity.literal() for entity in entities]

    @authorize_required
    def retrieve(self, key: str, **variables):
        entity = self.repository.find_one(key=key)

        return entity.literal()

    @authorize_required
    def create(self, dto: NoteDto, **variables):
        entity = self.repository.save(
            name=dto.name,
            status=dto.status
        )

        return entity.literal()

    @authorize_required
    def update(self, key: str, dto: NoteDto, **variables):
        self.repository.find_one(key=key)
        entity = self.repository.save(**dto.dict())

        return entity.literal()

    @authorize_required
    def delete(self, key: str, **variables):
        self.repository.find_one(key=key)
        self.repository.delete()


class KeywordUsecase(BaseUsecase):

    def __init__(self, repository: KeywordRepository):
        self.repository = repository
    
    @authorize_required
    def create(self, dto: KeywordDto, **variables) -> LiteralData:
        entity = self.repository.save(**dto.dict())

        return entity.literal()
    

    @authorize_required
    def update(self, key: int, dto: KeywordDto, **variables) -> LiteralData:
        self.repository.find_by_id(id=key)
        entity = self.repository.save(**dto.dict())

        return entity.literal()
    
    @authorize_required
    def delete(self, key: object, **variables) -> LiteralData:
        entity = self.repository.find_by_id(id=key)
        self.repository.delete()

        return entity.literal()
