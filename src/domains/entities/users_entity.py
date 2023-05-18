from pydantic import BaseModel, validator
from typing import Literal
from datetime import timedelta, datetime

from core.utils.data import JwtToken
from apps.users.exceptions import (
    InvalidTokenType,
    AuthTokenCannotRead
)
from core.utils.jwt import generate_jwt_token


class AuthToken(JwtToken):
    type: Literal['refresh', 'access']

    @validator('type', pre=True)
    def check_type_name(cls, v):
        if v == 'refresh' or v == 'access':
            return v
        raise InvalidTokenType()


class UserEntity(BaseModel):
    id: int
    username: str
    email: str
    isActive: bool
    isStaff: bool

    @property
    def refreshToken(self) -> 'AuthToken':
        if not self.isActive:
            raise AuthTokenCannotRead()

        _now = datetime.now()
        _exp = _now + timedelta(days=7)
        token = generate_jwt_token(_id=self.id, _exp=int(_exp.strftime('%s')), _at=int(_now.strftime('%s')))
        return AuthToken(type='refresh', value=token)

    @property
    def accessToken(self) -> 'AuthToken':
        if not self.isActive:
            raise AuthTokenCannotRead()
        
        _now = datetime.now()
        _exp = _now + timedelta(minutes=60)
        token = generate_jwt_token(_id=self.id, _exp=int(_exp.strftime('%s')), _at=int(_now.strftime('%s')))
        return AuthToken(type='access', value=token)
