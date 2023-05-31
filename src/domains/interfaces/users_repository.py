from typing import TypedDict, Type, Union, Optional

from core.repository import BaseRepository

from domains.entities.users_entity import (
    AuthSessionEntity,
    UserEntity,
    AuthTokenEntity
)


AuthSessionRepositoryContext = TypedDict('AuthSessionRepositoryContext', {
    'AuthSessionEntity': Type[AuthSessionEntity]
})


class AuthSessionRepository(BaseRepository):
    def __init__(self, context: AuthSessionRepositoryContext): ...
    def send_email(self, email: str, code: int) -> int: ...
    def save(self, **kwargs) -> AuthSessionEntity: ...
    def find_by_id(self, id: str, *args, **kwargs) -> AuthSessionEntity: ...
    def delete(self) -> None: ...


AuthTokenRepositoryContext = TypedDict('AuthTokenRepositoryContext', {
    'AuthTokenEntity': Type[AuthTokenEntity],
    'UserEntity': Type[UserEntity]
})

AuthTokenCachePolicy = TypedDict('AuthTokenCachePolicy', {
    'max_age': int
})


class AuthTokenRepository(BaseRepository):
    def __init__(self, context: AuthTokenRepositoryContext): ...
    def find_access_token_by_user_id(self, user_id: int, policy: AuthTokenCachePolicy) -> AuthTokenEntity: ...


UserRepositoryContext = TypedDict('UserRepositoryContext', {
    'UserEntity': Type[UserEntity]
})


UserCachePolicy = TypedDict('AuthTokenCachePolicy', {
    'max_age': int
})


class UserRepository(BaseRepository):
    def find_by_email(self, email: str) -> Union[UserEntity, None]: ...
    def save(self, **kwargs) -> UserEntity: ...
    def find_by_id(self, id: int): ...
