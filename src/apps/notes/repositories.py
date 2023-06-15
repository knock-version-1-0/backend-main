from domains.entities.notes_entity import KeywordEntity
from .models import (
    Note,
    Keyword,
)
from django.db import IntegrityError, transaction

from domains.interfaces.notes_repository import (
    NoteRepository as NoteRepositoryInterface,
    NoteRepositoryContext,
    KeywordRepository as KeywordRepositoryInterface,
    KeywordRepositoryContext
)
from core.exceptions import (
    DatabaseError,
)
from apps.notes.exceptions import (
    NoteDoesNotExistError,
    NoteNameIntegrityError,
    KeywordDoesNotExistError
)
from core.models import StatusChoice
from domains.constants import MAX_NOTE_LIST_LIMIT


class NoteRepository(NoteRepositoryInterface):
    queryset = Note.objects\
        .select_related('author')\
        .prefetch_related('keywords__parent')\
        .filter(status=StatusChoice.SAVE)
    
    def __init__(self, context: NoteRepositoryContext):
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
                        name__icontains=lookup.get('name', '')
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

        except Exception:
            raise NoteDoesNotExistError()

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
                note.update(**kwargs)

            except IntegrityError:
                raise NoteNameIntegrityError()

            except Exception as e:
                raise DatabaseError(e)

        else:
            try:
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
            self.set_model_instance(None)

        except Exception as e:
            raise DatabaseError(e)


class KeywordRepository(KeywordRepositoryInterface):
    queryset = Keyword.objects.all()

    def __init__(self, context: KeywordRepositoryContext):
        self.KeywordEntity = context['KeywordEntity']
    
    def find_by_id(self, id, *args, **kwargs):
        try:
            obj = self.queryset.select_related('note', 'parent').get(pk=id)
            self.set_model_instance(obj)
        except Keyword.DoesNotExist:
            raise KeywordDoesNotExistError()

        return self.KeywordEntity(
            id=obj.pk,
            noteId=obj.note.pk,
            posX=obj.pos_x,
            posY=obj.pos_y,
            text=obj.text,
            parentId=obj.parent if obj.parent is not None else None,
            status=obj.status,
            timestamp=obj.timestamp
        )
    
    def save(self, **kwargs) -> KeywordEntity:
        with transaction.atomic():
            note_id = kwargs.pop('note_id')
            try:
                note = Note.objects.get(pk=note_id)
            except Note.DoesNotExist:
                raise NoteDoesNotExistError()

            self.check_permission(note.editable_only)

            parent_id = kwargs.pop('parent_id')
            parent = None if not parent_id else Keyword.objects.get(pk=parent_id)

            keyword: Keyword = self.get_model_instance()
            if not keyword:
                keyword = Keyword.objects.create(
                    note=note,
                    parent=parent,
                    **kwargs
                )
            else:
                result = self.queryset.select_for_update().filter(pk=keyword.pk).update(
                    note=note,
                    parent=parent,
                    **kwargs
                )
                if not result:
                    raise DatabaseError()

                keyword = self.queryset.get(pk=keyword.pk)
                self.set_model_instance(keyword)

        return self.KeywordEntity(
            id=keyword.pk,
            noteId=note_id,
            posX=keyword.pos_x,
            posY=keyword.pos_y,
            text=keyword.text,
            parentId=parent_id,
            status=keyword.status,
            timestamp=keyword.timestamp
        )
    
    def delete(self):
        keyword: Keyword = self.get_model_instance()
        note: Note = keyword.note
        self.check_permission(note.editable_only)

        try:
            keyword.delete()
            self.set_model_instance(None)

        except Exception as e:
            raise DatabaseError(e)
