from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError


class NoteDoesNotExistError(ObjectDoesNotExist):
    message = "Note가 존재하지 않습니다."
    type = ObjectDoesNotExist
    def __init__(self, *args):
        super().__init__(self.message, *args)


class NoteNameIntegrityError(IntegrityError):
    message = "동일한 Author일 경우 Note.name을 중복해서 등록할 수 없습니다."
    type = IntegrityError
    def __init__(self, *args):
        super().__init__(self.message, *args)


class KeywordPosIdIntegrityError(IntegrityError):
    message = "동일한 Keyword 내에서 posId는 중복될 수 없습니다."
    type = IntegrityError
    def __init__(self, *args):
        super().__init__(self.message, *args)


class RepositoryAuthorizeError(AttributeError):
    message = "find_by 메소드를 호출하기 전에 authorize 메소드를 호출해야 합니다."
    type = AttributeError
    def __init__(self, *args):
        super().__init__(self.message, *args)
