import logging

from rest_framework.request import QueryDict
from core.utils.data import ApiPayload

from django.http.request import QueryDict
from rest_framework import status
from core.service import BaseService, error_wrapper

from adapters.dto.users_dto import (
    AuthEmailDto,
    UserDto,
    AuthVerificationDto,
    AuthTokenDto
)
from domains.usecases.users_usecase import (
    AuthSessionUsecase,
    AuthTokenUsecase,
    UserUsecase
)
from apps.users.exceptions import (
    EmailSendFailed,
    EmailAddrValidationError,
    AttemptLimitOver,
    AuthSessionExpired,
    AuthenticationFailed,
    AuthSessionDoesNotExist,
    RefreshTokenExpired,
    RefreshTokenRequired,
    UserInvalidError
)
from core.exceptions import (
    DatabaseError,
    ValidationError,
)


logger = logging.getLogger(__name__)


class AuthSessionService(BaseService):

    def __init__(self, usecase: AuthSessionUsecase):
        self.usecase = usecase
    
    def send_email(self, data: QueryDict):
        status_code = None
        parse = lambda o: AuthEmailDto(
            email=o['email'],
            at=o['at']
        )

        try:
            status_code = status.HTTP_200_OK
            obj = self.usecase.send_email(dto=parse(data))
        
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
        
        return (ApiPayload(status='OK', data=obj), status_code)
    
    def verify(self, data: QueryDict):
        status_code = None
        parse = lambda o: AuthVerificationDto(
            id=o['id'],
            email=o['email'],
            emailCode=o['emailCode'],
            currentTime=o['currentTime']
        )

        try:
            status_code = status.HTTP_200_OK
            obj = self.usecase.verify(dto=parse(data))
        
        except AttemptLimitOver as e:
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)
        
        except AuthSessionExpired as e:
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)
        
        except AuthenticationFailed as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            return error_wrapper(e, status_code)
        
        except AuthSessionDoesNotExist as e:
            status_code = status.HTTP_404_NOT_FOUND
            return error_wrapper(e, status_code)
        
        except DatabaseError as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        except Exception as e:
            logger.error(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        return (ApiPayload(status='OK', data=obj), status_code)


class AuthTokenService(BaseService):
    def __init__(self, usecase: AuthTokenUsecase):
        self.usecase = usecase
    
    def create(self, data: QueryDict, max_age: int):
        status_code = None
        parse = lambda o: AuthTokenDto(
            type=o['type'],
            value=o['value']
        )

        try:
            status_code = status.HTTP_200_OK
            obj = self.usecase.create(parse(data), max_age=max_age)
        
        except RefreshTokenRequired as e:
            logger.info(e)
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)
        
        except RefreshTokenExpired as e:
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)
        
        except UserInvalidError as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            return error_wrapper(e, status_code)
        
        except Exception as e:
            logger.error(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)

        return (ApiPayload(status='OK', data=obj), status_code)


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
            return error_wrapper(DatabaseError(e), status_code)

        return (ApiPayload(status='CREATED', data=obj), status_code)
