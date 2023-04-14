import logging
from typing import Tuple, Union, Optional
from core.utils.typing import StatusCode, Code

from django.http.request import QueryDict
from rest_framework import status
from core.service import BaseService, error_wrapper

from adapters.dto.notes_dto import (
    NoteDto,
    NoteReqDto,
    KeywordReqDto,
    NoteSummaryDto
)
from domains.usecases.notes_usecase import (
    NoteUsecase
)
from core.exceptions import (
    NoteDoesNotExistError,
    NoteNameIntegrityError,
    UserInvalidError,
    KeywordPosIdIntegrityError,
    DatabaseError,
    UserPermissionError
)

logger = logging.getLogger(__name__)

__all__ = [
    'NoteService',
]


class NoteService(BaseService):
    
    def __init__(self, usecase: NoteUsecase):
        self.usecase = usecase
    
    def list(self, params=None, user_id: Optional[int]=None) -> Tuple[Union[NoteSummaryDto, Code], StatusCode]:
        status_code = None

        try:
            status_code = status.HTTP_200_OK
            obj = self.usecase.list(params, user_id=user_id)
        
        except UserInvalidError as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            return error_wrapper(e, status_code)
        
        except DatabaseError as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)

        except Exception as e:
            logger.info(e)
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)

        return (obj, status_code)
    
    def retrieve(self, key: str, user_id: int) -> Tuple[Union[NoteDto, Code], StatusCode]:
        name = key
        status_code = None

        try:
            status_code = status.HTTP_200_OK
            obj = self.usecase.retrieve(key=name, user_id=user_id)

        except NoteDoesNotExistError as e:
            status_code = status.HTTP_404_NOT_FOUND
            return error_wrapper(e, status_code)
        
        except UserInvalidError as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            return error_wrapper(e, status_code)

        except UserPermissionError as e:
            status_code = status.HTTP_403_FORBIDDEN
            return error_wrapper(e, status_code)
        
        except DatabaseError as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        except Exception as e:
            logger.info(e)
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)

        return (obj, status_code)

    def create(self, req_body: QueryDict, user_id: int) -> Tuple[Union[NoteDto, Code], StatusCode]:
        status_code = None
        parse = lambda o: NoteReqDto(
            name=o['name'],
            keywords=o.get('keywords', []),
            status=o['status']
        )

        try:
            status_code = status.HTTP_200_OK
            obj = self.usecase.create(req_body=parse(req_body), user_id=user_id)
        
        except NoteNameIntegrityError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)
        
        except KeywordPosIdIntegrityError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)
        
        except UserInvalidError as e:
            status_code = status.HTTP_401_UNAUTHORIZED
            return error_wrapper(e, status_code)
        
        except UserPermissionError as e:
            status_code = status.HTTP_403_FORBIDDEN
            return error_wrapper(e, status_code)
        
        except DatabaseError as e:
            logger.debug(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return error_wrapper(e, status_code)
        
        except Exception as e:
            logger.info(e)
            status_code = status.HTTP_400_BAD_REQUEST
            return error_wrapper(e, status_code)
        
        return (obj, status_code)
