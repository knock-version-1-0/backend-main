from typing import TypedDict, Type, Union, overload

from core.repository import BaseRepository

from domains.entities.users_entity import (
    AuthSessionEntity,
)


AuthRepositoryContext = TypedDict('AuthRepositoryContext', {
    'AuthSessionEntity': Type[AuthSessionEntity]
})


class AuthRepository(BaseRepository):
    def __init__(self, context: AuthRepositoryContext): ...
    def send_email(self, email: str, code: int) -> None: ...
    def save(self,  **kwargs) -> AuthSessionEntity: ...
    @overload
    def find_by_email(self, email: str) -> AuthSessionEntity: ...
    @overload
    def find_by_email(self, email: str) -> None: ...
    def delete(self, key: str) -> None: ...
