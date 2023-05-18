from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import BadRequest, ValidationError


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


class EmailValidationError(Exception):
    message = "Email is invalid. Please check your email"
    error_type = ValidationError
    def __init__(self, *args):
        super().__init__(self.message, *args)


class AttemptLimitOver(Exception):
    message = "attempt는 최대 3회까지 가능합니다."
    error_type = BadRequest
    def __init__(self, *args):
        super().__init__(self.message, *args)
