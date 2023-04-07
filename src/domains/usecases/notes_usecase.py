from domains.interfaces.notes_repository import (
    NoteRepository
)
from domains.entities.exceptions import (
    NoteNameIntegrityError,
    KeywordPositionOrderIntegrityError,
    NoteDoesNotExistError,
    RepositoryAuthorizeError
)
from core.usecase import BaseUsecase


class NoteUsecase(BaseUsecase):
    def __init__(self, repository: NoteRepository, context: dict):
        self.note_repo = repository
        self.NoteResDto = context['NoteResDto']
        self.KeywordResDto = context['KeywordResDto']

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
            keywords=[self.KeywordResDto(order=k.order) for k in entity.keywords],
            status=entity.status
        )
