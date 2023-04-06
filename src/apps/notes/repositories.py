from .models import (
    Note,
    Keyword,
    Position,
)
from domains.interfaces.notes_repository import (
    NoteRepository as NoteRepositoryInterface
)
from core.models import StatusChoice

from django.db.models import Prefetch
from django.db.utils import IntegrityError


class NoteRepository(NoteRepositoryInterface):
    def __init__(self,
                 note_entity_cls,
                 keyword_entity_cls,
                 keyword_position_entity_cls):
        self.NoteEntity = note_entity_cls
        self.KeywordEntity = keyword_entity_cls
        self.KeywordPositionEntity = keyword_position_entity_cls

    def find_by_name(self, name):
        try:
            note = Note.objects.prefetch_related(
                Prefetch('keywords', queryset=Keyword.objects.prefetch_related('positions'))
            ).filter(status=StatusChoice.SAVE).get(name=name, author=self.user)
        except Note.DoesNotExist as e:
            raise e
        except IntegrityError as e:
            raise e

        self.set_model_instance(note)
        
        keywords = list(map(
            lambda x: self.KeywordEntity(
                positions=[self.KeywordPositionEntity(
                    order=position.order
                ) for position in x.positions.all()]
            ), note.keywords.all())
        )

        return self.NoteEntity(
            author_id=note.author,
            display_id=note.display_id,
            name=note.name,
            keywords=keywords,
            status=note.status
        )

    def save(self, **kwargs):
        instance = self.get_model_instance()

        if bool(instance):
            instance.update(**kwargs)
        else:
            Note.objects.create(**kwargs)
