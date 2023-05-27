import logging
from typing import Optional
from core.utils.data import ApiPayload

from django.http.request import QueryDict
from rest_framework import status
from core.service import BaseService, error_wrapper

from adapters.dto.users_dto import (
    AuthEmailDto,
)
from domains.usecases.users_usecase import (
    AuthUseCase,
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

    def __init__(self, usecase: AuthUseCase):
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
