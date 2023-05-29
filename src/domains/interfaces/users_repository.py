from typing import TypedDict, Type, Union

from core.repository import BaseRepository

from domains.entities.users_entity import (
    AuthSessionEntity,
    UserEntity
)


AuthRepositoryContext = TypedDict('AuthRepositoryContext', {
    'AuthSessionEntity': Type[AuthSessionEntity]
})


class AuthRepository(BaseRepository):
    def __init__(self, context: AuthRepositoryContext): ...
    def send_email(self, email: str, code: int) -> int: ...
    def save(self, **kwargs) -> AuthSessionEntity: ...
    def find_by_id(self, id: str, *args, **kwargs) -> AuthSessionEntity: ...
    def delete(self) -> None: ...


UserRepositoryContext = TypedDict('UserRepositoryContext', {
    'UserEntity': Type[UserEntity]
})


class UserRepository(BaseRepository):
    def find_by_email(self, email: str) -> Union[UserEntity, None]: ...
    def save(self, **kwargs) -> UserEntity: ...
