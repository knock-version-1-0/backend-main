from core.factory import BaseFactory

from apps.users.repositories import (
    AuthRepository
)
from domains.entities.users_entity import (
    AuthSessionEntity,
)
from domains.usecases.users_usecase import (
    AuthUseCase,
)
from adapters.services.users_service import (
    AuthService,
)
from adapters.controllers.users_controller import (
    AuthController,
)


class AuthFactory(BaseFactory):

    @property
    def repository(self) -> AuthRepository:
        return AuthRepository({
            'AuthSessionEntity': AuthSessionEntity,
        })
    
    @property
    def usecase(self) -> AuthUseCase:
        return AuthUseCase(
            self.repository
        )
    
    @property
    def service(self) -> AuthService:
        return AuthService(self.usecase)

    @property
    def controller(self) -> AuthController:
        return AuthController(self.service)
