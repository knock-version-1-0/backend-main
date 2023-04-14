import logging

from .models import (
    Note,
    Keyword,
)
from django.db import IntegrityError
from django.db import transaction

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
from domains.constants import MAX_NOTE_LIST_LIMIT

logger = logging.getLogger(__name__)

__all__ = [
    'NoteRepository',
]


class NoteRepository(NoteRepositoryInterface):
    queryset = Note.objects\
        .select_related('author')\
        .prefetch_related('keywords')\
        .filter(status=StatusChoice.SAVE)
    
    def __init__(self, context: dict):
        self.NoteEntity = context['NoteEntity']
        self.KeywordEntity = context['KeywordEntity']
        self.NoteSummaryEntity = context['NoteSummaryEntity']
    
    def find_by_author(self, lookup={}):
        try:
            offset, limit = lookup.get('offset', 0), lookup.get('limit', MAX_NOTE_LIST_LIMIT)
            if limit > MAX_NOTE_LIST_LIMIT:
                limit = MAX_NOTE_LIST_LIMIT

            notes = self.queryset.filter(
                        author=self.user,
                        name__contains=lookup.get('name', '')
                    )[offset:offset+limit]
        
        except Exception as e:
            logger.debug(e)
            raise DatabaseError(e)

        return [self.NoteSummaryEntity(
            displayId=note.display_id,
            name=note.name
        ) for note in notes]

    def find_one(self, display_id: str):
        try:
            note = self.queryset.get(display_id=display_id)

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
                with transaction.atomic():
                    keywords = kwargs.pop('keywords')
                    try:
                        note = self.queryset.create(
                            author=self.user,
                            **kwargs
                        )

                    except IntegrityError:
                        raise NoteNameIntegrityError()
                    
                    try:
                        keywords = [Keyword.objects.create(
                            note=note,
                            pos_id=k['posId'],
                            text=k.get('text')
                        ) for k in keywords]

                    except IntegrityError:
                        raise KeywordPosIdIntegrityError()

            except NoteNameIntegrityError as e:
                raise e
            
            except KeywordPosIdIntegrityError as e:
                raise e

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
                    text=k.text) for k in keywords],
                status=note.status
            )
