import logging
from core.utils.decorators import authorize_required

from core.usecase import BaseUsecase

from domains.interfaces.notes_repository import (
    NoteRepository
)
from core.exceptions import (
    NoteNameIntegrityError,
    NoteDoesNotExistError,
    AuthorizeNotCalledError,
    KeywordPosIdIntegrityError,
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

    @authorize_required
    def retrieve(self, key: str, user_id: int):
        try:
            entity = self.repository.find_by_display_id(display_id=key)

        except AuthorizeNotCalledError as e:
            logger.error(AuthorizeNotCalledError.message)
            raise e

        except NoteDoesNotExistError as e:
            raise e

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
        try:
            entity = self.repository.save(
                name=req_body.name,
                status=req_body.status,
                keywords=[k.dict() for k in req_body.keywords]
            )

        except AuthorizeNotCalledError as e:
            raise e
        
        except NoteNameIntegrityError as e:
            raise e
        
        except KeywordPosIdIntegrityError as e:
            raise e

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
