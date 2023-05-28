from typing import Optional, List
from rest_framework.request import QueryDict

from core.repository import BaseRepository
from core.crud import CRUDMixin
from core.utils.typing import LiteralData


class BaseUsecase(CRUDMixin):
    def __init__(self, repository: BaseRepository, context: Optional[dict]=None):
        self.repository = repository

    def list(self, params: Optional[QueryDict]=None, user_id: Optional[int]=None) -> List[LiteralData]:
        raise NotImplementedError()
    
    def retrieve(self, key: object, **variables) -> LiteralData:
        raise NotImplementedError()
    
    def create(self, data: object, **variables) -> LiteralData:
        raise NotImplementedError()
    
    def update(self, key: object, data: object, **variables) -> LiteralData:
        raise NotImplementedError()
    
    def delete(self, key: object, **variables) -> None:
        raise NotImplementedError()
