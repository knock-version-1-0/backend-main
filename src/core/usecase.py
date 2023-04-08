from core.repository import BaseRepository
from core.crud import CRUDMixin


class BaseUsecase(CRUDMixin):
    def __init__(self, repository: BaseRepository, context: dict):
        self.repository = repository
