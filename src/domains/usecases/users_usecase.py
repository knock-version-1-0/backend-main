from datetime import timedelta

from django.utils.crypto import get_random_string

from core.usecase import BaseUsecase
from core.utils.typing import Literal
from domains.entities.users_entity import (
    AuthSessionEntity
)
from adapters.dto.users_dto import (
    AuthEmailDto,
    AuthSessionDto,
    AuthVerificationDto,
    UserDto
)
from domains.interfaces.users_repository import (
    AuthRepository,
    UserRepository
)
from apps.users.exceptions import (
    EmailSendFailed,
    AuthenticationFailed
)


def _get_random_email_code():
    length = 6
    allowed_chars = '0123456789'
    return get_random_string(length, allowed_chars)


class AuthUsecase(BaseUsecase):
    __auth_session_period = timedelta(seconds=330)

    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def send_email(self, data: AuthEmailDto) -> Literal:
        auth_session_dto = self.generate_auth_session_data(data.email, data.at)
        entity = self.repository.save(
            **auth_session_dto.dict()
        )
        status = self.repository.send_email(
            email=entity.email,
            code=entity.emailCode
        )
        self.validate_email_transfer(status)

        return entity.literal()

    @classmethod
    def validate_email_transfer(cls, status):
        if status != 1:
            raise EmailSendFailed()

    @classmethod
    def validate_auth_session_period(cls, auth_session: AuthSessionEntity):
        period = cls.get_auth_session_period()
        assert auth_session.exp - auth_session.at == int(period.total_seconds())

    @classmethod
    def generate_auth_session_data(cls, email: str, at: int):
        period = cls.get_auth_session_period()
        return AuthSessionDto(
            email=email,
            emailCode=_get_random_email_code(),
            exp=at + int(period.total_seconds()),
            at=at,
            attempt=0
        )
    
    @classmethod
    def get_auth_session_period(cls) -> timedelta:
        return cls.__auth_session_period
    
    @classmethod
    def validate_email_code_input(cls, auth_session: AuthSessionEntity, auth_verification: AuthVerificationDto):
        if auth_session.emailCode != auth_verification.emailCode:
            raise AuthenticationFailed()


class UserUsecase(BaseUsecase):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create(self, data: UserDto, **variables) -> Literal:
        entity = self.repository.find_by_email(data.email)

        if not entity:
            entity = self.repository.save(username=data.email, email=data.email)
        
        data: Literal = {
            'refreshToken': entity.refreshToken.value,
            'accessToken': entity.accessToken.value
        }
        return data
