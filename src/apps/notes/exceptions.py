from django.core.exceptions import ObjectDoesNotExist, BadRequest
from django.db.utils import IntegrityError


class NoteDoesNotExistError(Exception):
    message = "Note should be existed when User retrieve"
    error_type = ObjectDoesNotExist
    def __init__(self, *args):
        super().__init__(self.message, *args)


class KeywordDoesNotExistError(Exception):
    message = "Keyword가 존재하지 않습니다."
    error_type = ObjectDoesNotExist
    def __init__(self, *args):
        super().__init__(self.message, *args)


class NoteNameIntegrityError(Exception):
    message = "Note.name shouldn't be duplicated when User update or create as same author"
    error_type = IntegrityError
    def __init__(self, *args):
        super().__init__(self.message, *args)


class NoteNameLengthLimitError(Exception):
    message = "Note list max length is {limit}"
    error_type = BadRequest
    def __init__(self, limit, *args):
        super().__init__(f"Note list max length is {limit}", *args)
