import logging

from rest_framework import exceptions, status
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class DatabaseError(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = _('DatabaseError')

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        logger.debug(detail)


class InternalServerError(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = _('InternalServerError')

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        logger.debug(detail)


class ValidationError(exceptions.ValidationError):
    default_code = _('ValidationError')

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        logger.error(detail)


class ExpiredSignatureError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = _('ExpiredSignatureError')
    default_detail = _("Token is expired")
