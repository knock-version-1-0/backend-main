from pydantic import BaseModel, validator
from typing import Literal
import uuid
from datetime import timedelta, datetime

from core.utils.data import JwtToken
from apps.users.exceptions import (
    InvalidTokenType,
    AuthTokenCannotRead
)
from core.utils.jwt import generate_jwt_token
from apps.users.exceptions import (
    AttemptLimitOver
)
from core.entity import BaseEntity


class AuthTokenEntity(JwtToken):
    type: Literal['refresh', 'access']

    @validator('type', pre=True)
    def check_type_name(cls, v):
        if v == 'refresh' or v == 'access':
            return v
        raise InvalidTokenType()


class UserEntity(BaseEntity):
    id: int
    username: str
    email: str
    isActive: bool
    isStaff: bool

    @property
    def refreshToken(self) -> 'AuthTokenEntity':
        if not self.isActive:
            raise AuthTokenCannotRead()

        _now = datetime.now()
        _exp = _now + timedelta(days=7)
        _type='refresh'
        token = generate_jwt_token(id=self.id, exp=int(_exp.strftime('%s')), at=int(_now.strftime('%s')), type=_type)
        return AuthTokenEntity(type=_type, value=token)

    @property
    def accessToken(self) -> 'AuthTokenEntity':
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
            return int(str)
        return v

    @validator('attempt')
    def check_attempt(cls, v):
        if v > 3:
            raise AttemptLimitOver()
