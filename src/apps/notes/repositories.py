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
)
from core.models import StatusChoice
from domains.constants import MAX_NOTE_LIST_LIMIT

__all__ = [
    'NoteRepository',
]


class NoteRepository(NoteRepositoryInterface):
    queryset = Note.objects\
        .select_related('author')\
        .prefetch_related('keywords__parent')\
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
            raise DatabaseError(e)

        return [self.NoteSummaryEntity(
            displayId=note.display_id,
            name=note.name
        ) for note in notes]

    def find_one(self, key: str):
        try:
            note = self.queryset.get(display_id=key)

        except Note.DoesNotExist:
            raise NoteDoesNotExistError()

        except Exception as e:
            raise DatabaseError(e)

        self.set_model_instance(note)
        self.check_permission(note.shared_only)

        return self.NoteEntity(
            id=note.pk,
            displayId=note.display_id,
            authorId=note.author.pk,
            name=note.name,
            keywords=[self.KeywordEntity(
                id=k.pk,
                noteId=note.pk,
                posX=k.pos_x,
                posY=k.pos_y,
                text=k.text,
                parentId=k.parent.pk if k.parent is not None else k.parent,
                status=k.status,
                timestamp=k.timestamp) for k in note.keywords.all()],
            status=note.status
        )

    def save(self, **kwargs):
        note: Note = self.get_model_instance()

        if bool(note):
            self.check_permission(note.author_only)

            try:
                with transaction.atomic():
                    note.update(**kwargs)

            except IntegrityError:
                raise NoteNameIntegrityError()

            except Exception as e:
                raise DatabaseError(e)

        else:
            try:
                with transaction.atomic():
                    note = Note.objects.create(
                        author=self.user,
                        **kwargs
                    )

            except IntegrityError:
                raise NoteNameIntegrityError()

            except Exception as e:
                raise DatabaseError(e)

        return self.NoteEntity(
            id=note.pk,
            displayId=note.display_id,
            authorId=note.author.pk,
            name=note.name,
            status=note.status
        )
    
    def delete(self):
        note: Note = self.get_model_instance()

        try:
            self.check_permission(note.author_only)
            note.delete()

        except Exception as e:
            raise DatabaseError(e)
