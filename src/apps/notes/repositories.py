from .models import (
    Note,
    Keyword,
    Position
)
from domains.interfaces.notes_repository import (
    NoteRepository as NoteRepositoryInterface
)

from django.db.models import Prefetch


class NoteRepository(NoteRepositoryInterface):
    def __init__(self,
                 note_entity_cls,
                 keyword_entity_cls,
                 keyword_position_entity_cls):
        self.NoteEntity = note_entity_cls
        self.KeywordEntity = keyword_entity_cls
        self.KeywordPositionEntity = keyword_position_entity_cls

    def find_by_name(self, name):
        note = Note.objects.prefetch_related(
            Prefetch('keywords', queryset=Keyword.objects.prefetch_related('positions'))
        ).get(name=name, author=self.user)
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
