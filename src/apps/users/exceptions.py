from rest_framework import exceptions, status


class UserInvalidError(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "User invalid"
    default_code = 'UserInvalidError'


class UserPermissionError(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "유저 접근 권한이 없습니다."
    default_code = 'UserPermissionError'


class InvalidTokenType(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Token type should be 'refresh' or 'access'"
    default_code = 'InvalidTokenType'


class AuthTokenCannotRead(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User는 isActive 상태일 때, token을 생성할 수 있습니다."
    default_code = 'AuthTokenCannotRead'


class EmailAddrValidationError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Email is invalid. Please check your email"
    default_code = 'EmailAddrValidationError'


class AttemptLimitOver(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "attempt는 최대 3회까지 가능합니다."
    default_code = 'AttemptLimitOver'


class EmailSendFailed(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Email을 보내지 못했습니다. Server의 system connection을 점검해주세요."
    default_code = 'EmailSendFailed'


class AuthenticationFailed(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Failed authentication"
    default_code = 'AuthenticationFailed'


class AuthSessionExpired(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Auth session is expired"
    default_code = 'AuthSessionExpired'


class AuthSessionDoesNotExist(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "해당 session이 존재하지 않거나 올바르지 않은 email입니다."
    default_code = 'AuthSessionDoesNotExist'


class RefreshTokenExpired(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "refresh token is expired please authenticate user."
    default_code = 'RefreshTokenExpired'


class RefreshTokenRequired(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Refresh token is required in request body"
    default_code = 'RefreshTokenRequired'
