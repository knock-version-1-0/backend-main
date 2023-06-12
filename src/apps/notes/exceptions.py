from rest_framework import exceptions, status
from django.utils.translation import gettext_lazy as _


class NoteDoesNotExistError(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("Note should be existed when User retrieve")
    default_code = _('NoteDoesNotExistError')


class KeywordDoesNotExistError(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("Keyword가 존재하지 않습니다.")
    default_code = _('KeywordDoesNotExistError')


class NoteNameIntegrityError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Note.name shouldn't be duplicated when User update or create as same author")
    default_code = _('NoteNameIntegrityError')


class NoteNameLengthLimitError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Note list max length is 25")
    default_code = _('NoteNameLengthLimitError')
