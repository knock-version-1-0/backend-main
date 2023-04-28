from core.factory import BaseFactory

from apps.notes.repositories import NoteRepository
from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity,
    NoteSummaryEntity,
)
from domains.usecases.notes_usecase import NoteUsecase
from adapters.services.notes_service import (
    NoteService,
)
from adapters.controllers.notes_controller import (
    NoteController,
)


class NoteFactory(BaseFactory):

    @property
    def repository(self) -> NoteRepository:
        return NoteRepository({
            'NoteEntity': NoteEntity,
            'KeywordEntity': KeywordEntity,
            'NoteSummaryEntity': NoteSummaryEntity
        })
    
    @property
    def usecase(self) -> NoteUsecase:
        return NoteUsecase(
            self.repository)

    @property
    def service(self) -> NoteService:
        return NoteService(self.usecase)

    @property
    def controller(self) -> NoteController:
        return NoteController(self.service)
