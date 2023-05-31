from core.factory import BaseFactory

from apps.users.repositories import (
    AuthSessionRepository,
    UserRepository,
    AuthTokenRepository,
)
from domains.entities.users_entity import (
    AuthSessionEntity,
    UserEntity,
    AuthTokenEntity,
)
from domains.usecases.users_usecase import (
    AuthSessionUsecase,
    UserUsecase,
    AuthTokenUsecase,
)
from adapters.services.users_service import (
    AuthSessionService,
    UserService,
    AuthTokenService,
)
from adapters.controllers.users_controller import (
    AuthSessionController,
    UserController,
    AuthTokenController,
)


class AuthSessionFactory(BaseFactory):

    @property
    def repository(self) -> AuthSessionRepository:
        return AuthSessionRepository({
            'AuthSessionEntity': AuthSessionEntity,
        })
    
    @property
    def usecase(self) -> AuthSessionUsecase:
        return AuthSessionUsecase(
            self.repository
        )
    
    @property
    def service(self) -> AuthSessionService:
        return AuthSessionService(self.usecase)

    @property
    def controller(self) -> AuthSessionController:
        return AuthSessionController(self.service)


class AuthTokenFactory(BaseFactory):

    @property
    def repository(self) -> AuthTokenRepository:
        return AuthTokenRepository({
            'AuthTokenEntity': AuthTokenEntity,
            'UserEntity': UserEntity
        })
    
    @property
    def usecase(self) -> AuthTokenUsecase:
        return AuthTokenUsecase(self.repository)
    
    @property
    def service(self) -> AuthTokenService:
        return AuthTokenService(self.usecase)
    
    @property
    def controller(self) -> AuthTokenController:
        return AuthTokenController(self.service)


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
