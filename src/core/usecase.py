from typing import Optional

from core.repository import BaseRepository
from core.crud import CRUDMixin


class BaseUsecase(CRUDMixin):
    def __init__(self, repository: BaseRepository, context: Optional[dict]=None):
        self.repository = repository
