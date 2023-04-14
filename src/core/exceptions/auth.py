from rest_framework.exceptions import PermissionDenied


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
