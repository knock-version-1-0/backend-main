from rest_framework import exceptions, status
from django.utils.translation import gettext_lazy as _


class UserInvalidError(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("User invalid")
    default_code = _('UserInvalidError')


class UserPermissionError(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("유저 접근 권한이 없습니다.")
    default_code = _('UserPermissionError')


class InvalidTokenType(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Token type should be 'refresh' or 'access'")
    default_code = _('InvalidTokenType')


class AuthTokenCannotRead(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("User는 isActive 상태일 때, token을 생성할 수 있습니다.")
    default_code = _('AuthTokenCannotRead')


class EmailAddrValidationError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Email is invalid. Please check your email")
    default_code = _('EmailAddrValidationError')


class AttemptLimitOver(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("attempt는 최대 3회까지 가능합니다.")
    default_code = _('AttemptLimitOver')


class EmailSendFailed(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Email을 보내지 못했습니다. Server의 system connection을 점검해주세요.")
    default_code = _('EmailSendFailed')


class AuthenticationFailed(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Failed authentication")
    default_code = _('AuthenticationFailed')


class AuthSessionExpired(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Auth session is expired")
    default_code = _('AuthSessionExpired')


class AuthSessionDoesNotExist(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("해당 session이 존재하지 않거나 올바르지 않은 email입니다.")
    default_code = _('AuthSessionDoesNotExist')


class RefreshTokenExpired(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("refresh token is expired please authenticate user.")
    default_code = _('RefreshTokenExpired')


class RefreshTokenRequired(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Refresh token is required in request body")
    default_code = _('RefreshTokenRequired')
