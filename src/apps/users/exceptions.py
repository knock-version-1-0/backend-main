from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import BadRequest


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


class InvalidTokenType(BadRequest):
    message = "Token type should be 'refresh' or 'access'"
    error_type = BadRequest
    def __init__(self, *args):
        super().__init__(self.message, *args)


class AuthTokenCannotRead(Exception):
    message = "User는 isActive 상태일 때, token을 생성할 수 있습니다."
    error_type = BadRequest
    def __init__(self, *args):
        super().__init__(self.message, *args)
