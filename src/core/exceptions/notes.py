from django.core.exceptions import ObjectDoesNotExist, BadRequest
from django.db.utils import IntegrityError


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


class NoteNameLengthLimitError(BadRequest):
    message = "Note name의 length는 {limit}를 초과할 수 없습니다."
    error_type = BadRequest
    def __init__(self, limit, *args):
        super().__init__(f"Note name의 length는 {limit}를 초과할 수 없습니다.", *args)
