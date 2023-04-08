from core.factory import BaseFactory

from apps.notes.repositories import NoteRepository
from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity
)
from domains.usecases.notes_usecase import NoteUsecase
from adapters.dto.notes_dto import (
    NoteDto,
    KeywordDto
)
from adapters.services.notes_service import (
    NoteService,
)
from adapters.controllers.notes_controller import (
    NoteController,
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
            'NoteDto': NoteDto,
            'KeywordDto': KeywordDto
        })

    @property
    def service(self):
        return NoteService(self.usecase)

    @property
    def controller(self):
        return NoteController(self.service)
