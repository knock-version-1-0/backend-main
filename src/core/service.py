from typing import Tuple, Optional, Union
from rest_framework.request import QueryDict
from rest_framework import status

from core.utils.data import (
    ErrorDetail,
    ApiPayload
)
from core.usecase import BaseUsecase
from core.exceptions import InternalServerError


success_code = {
    'OK': status.HTTP_200_OK,
    'CREATE': status.HTTP_200_OK,
    'UPDATE': status.HTTP_200_OK,
    'DELETE': status.HTTP_200_OK,
    'CREATED': status.HTTP_201_CREATED,
    'NO_CONTENT': status.HTTP_204_NO_CONTENT
}


class BaseService:
    dto_class = None

    def __init__(self, usecase: BaseUsecase):
        self.usecase = usecase

    def list(self, params: Optional[Union[QueryDict, dict]]=None, success='OK', **variables) -> Tuple[Union[ApiPayload, ErrorDetail], int]:
        obj = self.usecase.list(params=params, **variables)
        
        return (ApiPayload(status=success, data=obj), success_code[success])

    def retrieve(self, key: object, success='OK', **variables) -> Tuple[Union[ApiPayload, ErrorDetail], int]:
        obj = self.usecase.retrieve(key=key, **variables)

        return (ApiPayload(status=success, data=obj), success_code[success])

    def create(self, data: Union[QueryDict, dict], success='CREATED', **variables) -> Tuple[Union[ApiPayload, ErrorDetail], int]:
        obj = self.usecase.create(dto=self.parse(data), **variables)

        return (ApiPayload(status=success, data=obj), success_code[success])

    def update(self, key: object, data: Union[QueryDict, dict], success='OK', **variables) -> Tuple[Union[ApiPayload, ErrorDetail], int]:
        obj = self.usecase.update(key=key, dto=self.parse(data), **variables)

        return (ApiPayload(status=success, data=obj), success_code[success])
    
    def delete(self, key: object, success='NO_CONTENT', **variables) -> Tuple[Union[ApiPayload, ErrorDetail], int]:
        obj = self.usecase.delete(key=key, **variables)
        
        return (ApiPayload(status=success, data=obj), success_code[success])
    
    def _get_default_dto_class(self):
        if not self.dto_class:
            raise InternalServerError('Service have to set static dto class value')
        return self.dto_class
    
    def parse(self, data, dto_class=None):
        dto_class = self._get_default_dto_class() if not dto_class else dto_class
        return dto_class(**data)
