import logging
from core.utils.decorators import authorize_required

from core.usecase import BaseUsecase

from domains.interfaces.notes_repository import (
    NoteRepository
)

logger = logging.getLogger(__name__)

__all__ = [
    'NoteUsecase',
]


class NoteUsecase(BaseUsecase):

    def __init__(self, repository: NoteRepository, context: dict):
        self.repository = repository
        self.NoteDto = context['NoteDto']
        self.KeywordDto = context['KeywordDto']
        self.NoteSummaryDto = context['NoteSummaryDto']

    @authorize_required
    def list(self, lookup: dict={}):
        entities = self.repository.find_by_author(lookup=lookup)
        
        return [self.NoteSummaryDto(**entity.dict()) for entity in entities]

    @authorize_required
    def retrieve(self, key: str, user_id: int):
        entity = self.repository.find_one(display_id=key)

        return self.NoteDto(
            id=entity.id,
            displayId=entity.displayId,
            authorId=entity.authorId,
            name=entity.name,
            keywords=[self.KeywordDto(
                noteId=k.noteId,
                posId=k.posId,
                text=k.text) for k in entity.keywords],
            status=entity.status
        )

    @authorize_required
    def create(self, req_body, user_id: int):
        entity = self.repository.save(
            name=req_body.name,
            status=req_body.status,
            keywords=[k.dict() for k in req_body.keywords]
        )

        return self.NoteDto(
            id=entity.id,
            displayId=entity.displayId,
            authorId=entity.authorId,
            name=entity.name,
            keywords=[self.KeywordDto(
                noteId=k.noteId,
                posId=k.posId,
                text=k.text) for k in entity.keywords],
            status=entity.status
        )
