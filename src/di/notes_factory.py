from core.factory import BaseFactory
from apps.notes.repositories import NoteRepository
from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity
)
from domains.usecases.notes_usecase import NoteUsecase
from adapters.dto.notes_dto import (
    NoteResDto,
    KeywordResDto
)


class NoteFactory(BaseFactory):
    @property
    def repository(self):
        return NoteRepository({
            'NoteEntity': NoteEntity,
            'KeywordEntity': KeywordEntity
        })
    
    @property
    def usecase(self):
        return NoteUsecase(
            self.repository, {
            'NoteResDto': NoteResDto,
            'KeywordResDto': KeywordResDto
        })
