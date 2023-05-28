from pydantic import BaseModel

from core.utils.typing import LiteralData


class BaseEntity(BaseModel):
    def literal(self) -> LiteralData:
        _literal: LiteralData = self.dict()
        return _literal
