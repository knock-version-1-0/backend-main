from core.factory import BaseFactory

from apps.users.repositories import (
    AuthRepository,
    UserRepository,
)
from domains.entities.users_entity import (
    AuthSessionEntity,
    UserEntity,
)
from domains.usecases.users_usecase import (
    AuthUsecase,
    UserUsecase,
)
from adapters.services.users_service import (
    AuthService,
    UserService,
)
from adapters.controllers.users_controller import (
    AuthController,
    UserController,
)


class AuthFactory(BaseFactory):

    @property
    def repository(self) -> AuthRepository:
        return AuthRepository({
            'AuthSessionEntity': AuthSessionEntity,
        })
    
    @property
    def usecase(self) -> AuthUsecase:
        return AuthUsecase(
            self.repository
        )
    
    @property
    def service(self) -> AuthService:
        return AuthService(self.usecase)

    @property
    def controller(self) -> AuthController:
        return AuthController(self.service)


class UserFactory(BaseFactory):

    @property
    def repository(self) -> UserRepository:
        return UserRepository({
            'UserEntity': UserEntity,
        })
    
    @property
    def usecase(self) -> UserUsecase:
        return UserUsecase(self.repository)
    
    @property
    def service(self) -> UserService:
        return UserService(self.usecase)
    
    @property
    def controller(self) -> UserController:
        return UserController(self.service)
