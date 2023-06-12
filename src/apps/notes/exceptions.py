from rest_framework import exceptions, status


class NoteDoesNotExistError(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Note should be existed when User retrieve"
    default_code = 'NoteDoesNotExistError'


class KeywordDoesNotExistError(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Keyword가 존재하지 않습니다."
    default_code = 'KeywordDoesNotExistError'


class NoteNameIntegrityError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Note.name shouldn't be duplicated when User update or create as same author"
    default_code = 'NoteNameIntegrityError'


class NoteNameLengthLimitError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Note list max length is 25"
    default_code = 'NoteNameLengthLimitError'
