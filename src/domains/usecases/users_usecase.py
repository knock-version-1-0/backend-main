import logging
import uuid
from datetime import timedelta

from django.utils.crypto import get_random_string

from core.usecase import BaseUsecase
from domains.entities.users_entity import (
    AuthSessionEntity
)


def _get_random_email_code():
    length = 6
    allowed_chars = '0123456789'
    return get_random_string(length, allowed_chars)


class AuthUseCase(BaseUsecase):
    __period = timedelta(seconds=330)

    @classmethod
    def validate_auth_session_period(cls, auth_session: AuthSessionEntity):
        assert auth_session.exp - auth_session.at == int(cls.__period.total_seconds())

    @classmethod
    def generate_auth_session(cls, email: str, at: int):

        return AuthSessionEntity(
            id=uuid.uuid4(),
            email=email,
            emailCode=_get_random_email_code(),
            exp=at + int(cls.__period.total_seconds()),
            at=at,
            attempt=1
        )
