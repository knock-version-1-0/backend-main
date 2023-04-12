import logging

from .models import (
    Note,
    Keyword,
)
from django.db import IntegrityError

from domains.interfaces.notes_repository import (
    NoteRepository as NoteRepositoryInterface
)
from core.exceptions import (
    DatabaseError,
    NoteDoesNotExistError,
    NoteNameIntegrityError,
    KeywordPosIdIntegrityError
)
from core.models import StatusChoice

logger = logging.getLogger(__name__)

__all__ = [
    'NoteRepository',
]


class NoteRepository(NoteRepositoryInterface):
    def __init__(self, context: dict):
        self.NoteEntity = context['NoteEntity']
        self.KeywordEntity = context['KeywordEntity']

    def find_by_display_id(self, display_id: str):
        try:
            note = Note.objects.select_related('author')\
                .prefetch_related('keywords')\
                .filter(status=StatusChoice.SAVE)\
                .get(display_id=display_id)

        except Note.DoesNotExist:
            raise NoteDoesNotExistError()

        except Exception as e:
            logger.debug(e)
            raise DatabaseError(e)

        self.set_model_instance(note)
        self.check_permission()

        return self.NoteEntity(
            id=note.pk,
            displayId=note.display_id,
            authorId=note.author.pk,
            name=note.name,
            keywords=[self.KeywordEntity(
                noteId=k.note.id,
                posId=k.pos_id,
                text=k.text) for k in note.keywords.all()],
            status=note.status
        )

    def save(self, **kwargs):
        instance = self.get_model_instance()

        # Check

        if bool(instance):
            self.check_permission()
            instance.update(**kwargs)
        else:
            try:
                note = Note.objects.create(author=self.user, **kwargs)

            except IntegrityError as e:
                if e.args[0] == Note.__name__:
                    raise NoteNameIntegrityError()
                elif e.args[0] == Keyword.__name__:
                    raise KeywordPosIdIntegrityError()
                else:
                    raise DatabaseError(e)

            except Exception as e:
                logger.debug(e)
                raise DatabaseError(e)

            return self.NoteEntity(
                id=note.pk,
                displayId=note.display_id,
                authorId=note.author.pk,
                name=note.name,
                keywords=[self.KeywordEntity(
                    noteId=k.note.id,
                    posId=k.pos_id,
                    text=k.text) for k in note.keywords.all()],
                status=note.status
            )
