import logging
from typing import Optional
from core.data import ApiPayload

from django.http.request import QueryDict
from rest_framework import status
from core.service import BaseService, error_wrapper

from adapters.dto.notes_dto import (
    NoteReqDto,
    KeywordReqDto,
)
from domains.usecases.notes_usecase import (
    NoteUsecase
)
from core import exceptions


logger = logging.getLogger(__name__)

__all__ = [
    'NoteService',
]


class NoteService(BaseService):
    
    def __init__(self, usecase: NoteUsecase):
        self.usecase = usecase
    
    def list(self, params: Optional[QueryDict]=None, user_id: Optional[int]=None):
        status_code = None

        try:
            status_code = status.HTTP_200_OK
            obj = self.usecase.list(params, user_id=user_id)
        
        except exceptions.users.UserInvalidError as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            return error_wrapper(e, status_code)
        
        except exceptions.DatabaseError as e:
            logger.error(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)

        except Exception as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)

        return (ApiPayload(status='OK', data=obj), status_code)
    
    def retrieve(self, key: str, user_id: int):
        name = key
        status_code = None

        try:
            status_code = status.HTTP_200_OK
            obj = self.usecase.retrieve(key=name, user_id=user_id)

        except exceptions.notes.NoteDoesNotExistError as e:
            status_code = status.HTTP_404_NOT_FOUND
            return error_wrapper(e, status_code)
        
        except exceptions.users.UserInvalidError as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            return error_wrapper(e, status_code)

        except exceptions.users.UserPermissionError as e:
            status_code = status.HTTP_403_FORBIDDEN
            return error_wrapper(e, status_code)
        
        except exceptions.DatabaseError as e:
            logger.error(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        except Exception as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)

        return (ApiPayload(status='OK', data=obj), status_code)
    
    def update(self, key: str, req_body: QueryDict, user_id: int):
        status_code = None
        parse = lambda o: NoteReqDto(**o)

        try:
            status_code = status.HTTP_200_OK
            obj = self.usecase.update(key=key, req_body=parse(req_body), user_id=user_id)
        
        except exceptions.notes.NoteNameIntegrityError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)
        
        except exceptions.notes.NoteNameLengthLimitError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)
        
        except exceptions.users.UserInvalidError as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            return error_wrapper(e, status_code)
        
        except exceptions.users.UserPermissionError as e:
            status_code = status.HTTP_403_FORBIDDEN
            return error_wrapper(e, status_code)
        
        except exceptions.notes.NoteDoesNotExistError as e:
            status_code = status.HTTP_404_NOT_FOUND
            return error_wrapper(e, status_code)
        
        except exceptions.DatabaseError as e:
            logger.error(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        except Exception as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)

        return (ApiPayload(status='OK', data=obj), status_code)

    def create(self, req_body: QueryDict, user_id: int):
        status_code = None
        parse = lambda o: NoteReqDto(
            name=o['name'],
            status=o['status']
        )

        try:
            status_code = status.HTTP_201_CREATED
            obj = self.usecase.create(req_body=parse(req_body), user_id=user_id)
        
        except exceptions.notes.NoteNameIntegrityError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)
        
        except exceptions.users.UserInvalidError as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            return error_wrapper(e, status_code)
        
        except exceptions.users.UserPermissionError as e:
            status_code = status.HTTP_403_FORBIDDEN
            return error_wrapper(e, status_code)
        
        except exceptions.DatabaseError as e:
            logger.error(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        except Exception as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        return (ApiPayload(status='CREATED', data=obj), status_code)
    
    def delete(self, key: str, user_id: int):
        status_code = None

        try:
            status_code = status.HTTP_204_NO_CONTENT
            obj = self.usecase.delete(key=key, user_id=user_id)
        
        except exceptions.users.UserInvalidError as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            return error_wrapper(e, status_code)
        
        except exceptions.users.UserPermissionError as e:
            status_code = status.HTTP_403_FORBIDDEN
            return error_wrapper(e, status_code)
        
        except exceptions.notes.NoteDoesNotExistError as e:
            status_code = status.HTTP_404_NOT_FOUND
            return error_wrapper(e, status_code)
        
        except exceptions.DatabaseError as e:
            logger.error(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        except Exception as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)

        return (ApiPayload(status='NO_CONTENT', data=obj), status_code)
