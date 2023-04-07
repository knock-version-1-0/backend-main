from domains.interfaces.notes_repository import (
    NoteRepository
)
from domains.entities.exceptions import (
    NoteNameIntegrityError,
    NoteDoesNotExistError,
    RepositoryAuthorizeError,
    KeywordPosIdIntegrityError,
    IntegrityError
)
from core.usecase import BaseUsecase


class NoteUsecase(BaseUsecase):
    def __init__(self, repository: NoteRepository, context: dict):
        self.note_repo = repository
        self.NoteResDto = context['NoteResDto']
        self.KeywordBaseDto = context['KeywordBaseDto']

    def retrieve(self, key: str, user_id: int):
        self.note_repo.authorize(user_id)

        try:
            entity = self.note_repo.find_by_name(name=key)
        except NoteDoesNotExistError.type:
            raise NoteDoesNotExistError()
        except RepositoryAuthorizeError.type:
            raise RepositoryAuthorizeError()

        return self.NoteResDto(
            displayId=entity.displayId,
            authorId=entity.authorId,
            name=entity.name,
            keywords=[self.KeywordBaseDto(posId=k.posId) for k in entity.keywords],
            status=entity.status
        )

    def create(self, req_body, user_id):
        self.note_repo.authorize(user_id)

        try:
            self.note_repo.save(
                display_id=req_body.displayId,
                name=req_body.name,
                status=req_body.status,
                keywords=[k.dict() for k in req_body.keywords]
            )
        except RepositoryAuthorizeError.type:
            raise RepositoryAuthorizeError()
        except IntegrityError as e:
            if e.args[0] == 'note_integrity_error':
                raise NoteNameIntegrityError()
            if e.args[0] == 'keyword_integrity_error':
                raise KeywordPosIdIntegrityError()
