from rest_framework.exceptions import PermissionDenied


class AuthorizeNotCalledError(AttributeError):
    message = "find_by 메소드를 호출하기 전에 authorize 메소드를 호출해야 합니다."
    error_type = AttributeError
    def __init__(self, *args):
        super().__init__(self.message, *args)


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
