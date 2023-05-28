import logging

from rest_framework.request import QueryDict
from core.utils.data import ApiPayload, ErrorDetail

from django.http.request import QueryDict
from rest_framework import status
from core.service import BaseService, error_wrapper

from adapters.dto.users_dto import (
    AuthEmailDto,
    UserDto
)
from domains.usecases.users_usecase import (
    AuthUsecase,
    UserUsecase
)
from apps.users.exceptions import (
    EmailSendFailed,
    EmailAddrValidationError,
)
from core.exceptions import (
    DatabaseError,
    ValidationError,
)


logger = logging.getLogger(__name__)

__all__ = [
    'AuthService',
]


class AuthService(BaseService):

    def __init__(self, usecase: AuthUsecase):
        self.usecase = usecase
    
    def send_email(self, data: QueryDict):
        status_code = None
        parse = lambda o: AuthEmailDto(
            email=o['email'],
            at=o['at']
        )

        try:
            status_code = status.HTTP_200_OK
            obj = self.usecase.send_email(data=parse(data))
        
        except EmailAddrValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)

        except EmailSendFailed as e:
            logger.error(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        except DatabaseError as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        return (ApiPayload(status='CREATED', data=obj), status_code)


class UserService(BaseService):
    def __init__(self, usecase: UserUsecase):
        self.usecase = usecase

    def create(self, data: QueryDict, **variables):
        status_code = None
        parse = lambda o: UserDto(
            email=o['email']
        )

        try:
            status_code = status.HTTP_201_CREATED
            obj = self.usecase.create(parse(data))
        
        except Exception as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)

        return (ApiPayload(status='CREATED', data=obj), status_code)
