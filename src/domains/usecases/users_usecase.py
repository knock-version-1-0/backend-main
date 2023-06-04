from django.utils.crypto import get_random_string

from core.usecase import BaseUsecase
from core.utils.typing import LiteralData
from core.utils.jwt import parse_jwt_token
from domains.entities.users_entity import (
    AuthSessionEntity
)
from adapters.dto.users_dto import (
    AuthEmailDto,
    AuthSessionDto,
    AuthVerificationDto,
    UserDto,
    AuthTokenDto
)
from domains.interfaces.users_repository import (
    AuthSessionRepository,
    UserRepository,
    AuthTokenRepository
)
from apps.users.exceptions import (
    EmailSendFailed,
    AuthenticationFailed,
    AuthSessionDoesNotExist,
    AuthSessionExpired,
    AttemptLimitOver,
    RefreshTokenExpired,
    RefreshTokenRequired
)
from core.exceptions import ExpiredSignatureError


def _get_random_email_code():
    length = 6
    allowed_chars = '0123456789'
    return get_random_string(length, allowed_chars)


class AuthSessionUsecase(BaseUsecase):

    def __init__(self, repository: AuthSessionRepository):
        self.repository = repository

    def send_email(self, dto: AuthEmailDto) -> LiteralData:
        auth_session_dto = self.generate_auth_session_data(dto.email, dto.at)
        entity = self.repository.save(
            **auth_session_dto.dict()
        )
        status = self.repository.send_email(
            email=entity.email,
            code=entity.emailCode
        )
        self.validate_email_transfer(status)

        return entity.literal()
    
    def verify(self, dto: AuthVerificationDto) -> LiteralData:
        entity = self.repository.find_by_id(id=dto.id)
        self.validate_session_data_email(entity, dto)
        self.validate_session_expired(entity, dto)

        try:
            self.validate_email_code_input(entity, dto)
        except AuthenticationFailed as e:
            if entity.attempt >= 2:
                self.repository.delete()
                raise AttemptLimitOver()
            self.repository.save(attempt=entity.attempt + 1)
            raise e

        self.repository.delete()
        ret: LiteralData = {}
        return ret

    @classmethod
    def validate_email_transfer(cls, status):
        if status != 1:
            raise EmailSendFailed()

    @classmethod
    def validate_auth_session_period(cls, auth_session: AuthSessionEntity):
        period = AuthSessionEntity.get_expire_period()
        assert auth_session.exp - auth_session.at == int(period.total_seconds())

    @classmethod
    def generate_auth_session_data(cls, email: str, at: int):
        period = AuthSessionEntity.get_expire_period()
        return AuthSessionDto(
            email=email,
            emailCode=_get_random_email_code(),
            exp=at + int(period.total_seconds()),
            at=at,
            attempt=0
        )
    
    @classmethod
    def validate_email_code_input(cls, auth_session: AuthSessionEntity, auth_verification: AuthVerificationDto):
        if auth_session.emailCode != auth_verification.emailCode:
            raise AuthenticationFailed()
    
    @classmethod
    def validate_session_data_email(cls, auth_session: AuthSessionEntity, auth_verification: AuthVerificationDto):
        if auth_session.email != auth_verification.email:
            raise AuthSessionDoesNotExist()
    
    @classmethod
    def validate_session_expired(cls, auth_session: AuthSessionEntity, auth_verification: AuthVerificationDto):
        exp = auth_session.exp
        if auth_verification.currentTime > exp:
            raise AuthSessionExpired()


class AuthTokenUsecase(BaseUsecase):
    def __init__(self, repository: AuthTokenRepository):
        self.repository = repository
    
    def create(self, dto: AuthTokenDto, max_age: int) -> LiteralData:
        self.validate_refresh_token_type(dto)
        refresh_token = dto.value

        try:
            jwt_data = parse_jwt_token(refresh_token)
        except ExpiredSignatureError:
            raise RefreshTokenExpired()

        entity = self.repository.find_access_token_by_user_id(user_id=jwt_data['id'], policy={'max_age': max_age})
        return entity.literal()
    
    @classmethod
    def validate_refresh_token_type(cls, auth_token_dto: AuthTokenDto):
        if auth_token_dto.type != 'refresh':
            raise RefreshTokenRequired()


class UserUsecase(BaseUsecase):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create(self, dto: UserDto, **variables) -> LiteralData:
        entity = self.repository.find_by_email(dto.email)

        if not entity:
            entity = self.repository.save(username=dto.email, email=dto.email)
        
        dto: LiteralData = {
            'refreshToken': entity.refreshToken.value,
            'accessToken': entity.accessToken.value
        }
        return dto
