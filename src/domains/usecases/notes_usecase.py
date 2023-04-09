import logging
from core.utils.decorators import authorize_required

from core.usecase import BaseUsecase

from domains.interfaces.notes_repository import (
    NoteRepository
)
from domains.exceptions import (
    NoteNameIntegrityError,
    NoteDoesNotExistError,
    AuthorizeNotCalledError,
    KeywordPosIdIntegrityError,
    IntegrityError,
    DatabaseError
)
from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity,
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
            entity = self.repository.find_by_name(name=key)

        except AuthorizeNotCalledError.error_type:
            logger.error(AuthorizeNotCalledError.message)
            raise AuthorizeNotCalledError()

        except NoteDoesNotExistError.error_type:
            raise NoteDoesNotExistError()
        
        except Exception as e:
            logger.debug(e)
            raise DatabaseError()

        return self.NoteDto(
            id=entity.id,
            displayId=entity.displayId,
            authorId=entity.authorId,
            name=entity.name,
            keywords=[self.KeywordDto(noteId=k.noteId, posId=k.posId) for k in entity.keywords],
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

        except AuthorizeNotCalledError.error_type:
            raise AuthorizeNotCalledError()

        except IntegrityError as e:
            if e.args[0] == NoteEntity.__name__.replace('Entity', ''):
                raise NoteNameIntegrityError()
            if e.args[0] == KeywordEntity.__name__.replace('Entity', ''):
                raise KeywordPosIdIntegrityError()
        
        except Exception as e:
            logger.debug(e)
            raise DatabaseError()

        return self.NoteDto(
            id=entity.id,
            displayId=entity.displayId,
            authorId=entity.authorId,
            name=entity.name,
            keywords=[self.KeywordDto(noteId=k.noteId, posId=k.posId) for k in entity.keywords],
            status=entity.status
        )
