from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import BadRequest, ValidationError, ObjectDoesNotExist


class UserInvalidError(Exception):
    message = "User invalid"
    error_type = Exception
    def __init__(self, *args):
        super().__init__(self.message, *args)


class UserPermissionError(Exception):
    message = "유저 접근 권한이 없습니다."
    error_type = PermissionDenied
    def __init__(self, *args):
        super().__init__(self.message, *args)


class InvalidTokenType(Exception):
    message = "Token type should be 'refresh' or 'access'"
    error_type = BadRequest
    def __init__(self, *args):
        super().__init__(self.message, *args)


class AuthTokenCannotRead(Exception):
    message = "User는 isActive 상태일 때, token을 생성할 수 있습니다."
    error_type = BadRequest
    def __init__(self, *args):
        super().__init__(self.message, *args)


class EmailAddrValidationError(Exception):
    message = "Email is invalid. Please check your email"
    error_type = ValidationError
    def __init__(self, *args):
        super().__init__(self.message, *args)


class AttemptLimitOver(Exception):
    message = "attempt는 최대 3회까지 가능합니다."
    error_type = BadRequest
    def __init__(self, *args):
        super().__init__(self.message, *args)


class EmailSendFailed(Exception):
    message = "Email을 보내지 못했습니다. Server의 system connection을 점검해주세요."
    error_type = Exception
    def __init__(self, *args):
        super().__init__(self.message, *args)


class AuthenticationFailed(Exception):
    message = "Failed authentication"
    error_type = Exception
    def __init__(self, *args):
        super().__init__(self.message, *args)


class AuthSessionExpired(Exception):
    message = "Auth session is expired"
    error_type = BadRequest
    def __init__(self, *args):
        super().__init__(self.message, *args)


class AuthSessionDoesNotExist(Exception):
    message = "해당 session이 존재하지 않거나 올바르지 않은 email입니다."
    error_type = ObjectDoesNotExist
    def __init__(self, *args):
        super().__init__(self.message, *args)
