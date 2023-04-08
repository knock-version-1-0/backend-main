from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError, DatabaseError as _DatabaseError


class NoteDoesNotExistError(ObjectDoesNotExist):
    message = "Note가 존재하지 않습니다."
    error_type = ObjectDoesNotExist
    def __init__(self, *args):
        super().__init__(self.message, *args)


class NoteNameIntegrityError(IntegrityError):
    message = "동일한 Author일 경우 Note.name을 중복해서 등록할 수 없습니다."
    error_type = IntegrityError
    def __init__(self, *args):
        super().__init__(self.message, *args)


class KeywordPosIdIntegrityError(IntegrityError):
    message = "동일한 Keyword 내에서 posId는 중복될 수 없습니다."
    error_type = IntegrityError
    def __init__(self, *args):
        super().__init__(self.message, *args)


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


class DatabaseError(_DatabaseError):
    message = "Database error"
    error_type = _DatabaseError
    def __init__(self, *args):
        super().__init__(self.message, *args)
