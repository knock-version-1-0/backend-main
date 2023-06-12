from rest_framework.request import QueryDict
from django.http.request import QueryDict

from core.service import BaseService, success_code
from core.utils.data import ApiPayload
from adapters.dto.users_dto import (
    AuthEmailDto,
    UserDto,
    AuthVerificationDto,
    AuthTokenDto
)
from domains.usecases.users_usecase import (
    AuthSessionUsecase,
)


class AuthSessionService(BaseService):

    def __init__(self, usecase: AuthSessionUsecase):
        self.usecase = usecase
    
    def send_email(self, data: QueryDict, success='OK'):
        obj = self.usecase.send_email(dto=self.parse(data, AuthEmailDto))

        return (ApiPayload(status=success, data=obj), success_code[success])
    
    def verify(self, data: QueryDict, success='OK'):
        obj = self.usecase.verify(dto=self.parse(data, AuthVerificationDto))
        
        return (ApiPayload(status=success, data=obj), success_code[success])


class AuthTokenService(BaseService):
    dto_class = AuthTokenDto
    
    def create(self, data: QueryDict, success='OK', max_age: int=None):
        return super().create(data=data, success=success, max_age=max_age)


class UserService(BaseService):
    dto_class = UserDto
