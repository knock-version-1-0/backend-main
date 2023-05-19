from pydantic import BaseModel

from core.utils.typing import Literal


class BaseEntity(BaseModel):
    def literal(self) -> Literal:
        _literal: Literal = self.dict()
        return _literal
