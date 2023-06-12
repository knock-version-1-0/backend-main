import logging

from rest_framework import exceptions, status

logger = logging.getLogger(__name__)


class DatabaseError(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 'DatabaseError'

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        logger.debug(detail)


class InternalServerError(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 'InternalServerError'

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        logger.debug(detail)


class ValidationError(exceptions.ValidationError):
    default_code = 'ValidationError'

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        logger.error(detail)


class ExpiredSignatureError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'ExpiredSignatureError'
    default_detail = "Token is expired"
