from pydantic import validator
from dataclasses import dataclass, asdict
from typing import Literal
import uuid
from datetime import timedelta, datetime

from core.utils.typing import LiteralData
from core.utils.jwt import generate_jwt_token

from apps.users.exceptions import (
    InvalidTokenType,
    AuthTokenCannotRead
)
from apps.users.exceptions import (
    AttemptLimitOver
)
from core.entity import BaseEntity


@dataclass
class AuthTokenEntity:
    type: Literal['refresh', 'access']
    value: str

    def __post_init__(self):
        self.check_type_name()

    def check_type_name(self):
        if self.type not in ('refresh', 'access'):
            raise InvalidTokenType()
    
    def literal(self) -> LiteralData:
        ret: LiteralData = asdict(self)
        return ret


class UserEntity(BaseEntity):
    id: int
    username: str
    email: str
    isActive: bool
    isStaff: bool

    @property
    def refreshToken(self):
        if not self.isActive:
            raise AuthTokenCannotRead()

        _now = datetime.now()
        _exp = _now + timedelta(days=7)
        _type='refresh'
        token = generate_jwt_token(id=self.id, exp=int(_exp.strftime('%s')), at=int(_now.strftime('%s')), type=_type)
        return AuthTokenEntity(type=_type, value=token)

    @property
    def accessToken(self):
        if not self.isActive:
            raise AuthTokenCannotRead()
        
        _now = datetime.now()
        _exp = _now + timedelta(minutes=60)
        _type='access'
        token = generate_jwt_token(id=self.id, exp=int(_exp.strftime('%s')), at=int(_now.strftime('%s')), type=_type)
        return AuthTokenEntity(type=_type, value=token)


class AuthSessionEntity(BaseEntity):
    id: str
    email: str
    emailCode: str
    exp: int
    at: int
    attempt: int

    @validator('id', pre=True)
    def uuid_to_str(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    @validator('exp', 'at', pre=True)
    def str_to_int(cls, v):
        if isinstance(v, str):
            return int(v)
        return v

    @validator('attempt')
    def check_attempt(cls, v):
        if v > 3:
            raise AttemptLimitOver()
        return v
    
    def get_expire_period() -> timedelta:
        return timedelta(seconds=330)
