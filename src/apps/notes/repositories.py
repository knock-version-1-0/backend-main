from .models import (
    Note,
    Keyword,
)
from domains.interfaces.notes_repository import (
    NoteRepository as NoteRepositoryInterface
)
from core.models import StatusChoice

from django.db.utils import IntegrityError


class NoteRepository(NoteRepositoryInterface):
    def __init__(self,
                 note_entity_cls,
                 keyword_entity_cls):
        self.NoteEntity = note_entity_cls
        self.KeywordEntity = keyword_entity_cls

    def find_by_name(self, name):
        try:
            note = Note.objects.prefetch_related('keywords').filter(
                status=StatusChoice.SAVE
            ).get(name=name, author=self.user)
        except Note.DoesNotExist as e:
            raise e
        except IntegrityError as e:
            raise e

        self.set_model_instance(note)

        return self.NoteEntity(
            displayId=note.display_id,
            authorId=note.author,
            name=note.name,
            keywords=[self.KeywordEntity(noteId=k.note.id, order=k.order) for k in note.keywords.all()],
            status=note.status
        )

    def save(self, **kwargs):
        instance = self.get_model_instance()

        if bool(instance):
            instance.update(**kwargs)
        else:
            Note.objects.create(**kwargs)
