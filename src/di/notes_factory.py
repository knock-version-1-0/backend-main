from core.factory import BaseFactory

from apps.notes.repositories import NoteRepository, KeywordRepository
from domains.entities.notes_entity import (
    NoteEntity,
    KeywordEntity,
    NoteSummaryEntity,
)
from domains.usecases.notes_usecase import NoteUsecase, KeywordUsecase
from adapters.services.notes_service import (
    NoteService,
    KeywordService
)
from adapters.controllers.notes_controller import (
    NoteController,
    KeywordController
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


class KeywordFactory(BaseFactory):

    @property
    def repository(self) -> KeywordRepository:
        return KeywordRepository({
            'KeywordEntity': KeywordEntity
        })

    @property
    def usecase(self) -> KeywordUsecase:
        return KeywordUsecase(self.repository)

    @property
    def service(self) -> KeywordService:
        return KeywordService(self.usecase)
    
    @property
    def controller(self) -> KeywordController:
        return KeywordController(self.service)
