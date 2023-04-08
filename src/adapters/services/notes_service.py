from rest_framework import status

from adapters.dto.notes_dto import (
    NoteDto,
    KeywordDto,
    NoteReqDto,
)
from domains.usecases.notes_usecase import (
    NoteUsecase
)
from domains.exceptions import (
    NoteDoesNotExistError,
    NoteNameIntegrityError,
    AuthorizeNotCalledError,
    RepositoryAuthorizeError,
    KeywordPosIdIntegrityError,
)
