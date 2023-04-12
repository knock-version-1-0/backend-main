from .models import (
    Note,
    Keyword,
)

from domains.interfaces.notes_repository import (
    NoteRepository as NoteRepositoryInterface
)

from core.models import StatusChoice

__all__ = [
    'NoteRepository',
]


class NoteRepository(NoteRepositoryInterface):
    def __init__(self, context: dict):
        self.NoteEntity = context['NoteEntity']
        self.KeywordEntity = context['KeywordEntity']

    def find_by_name(self, name):
        note = Note.objects.prefetch_related('keywords').filter(
            status=StatusChoice.SAVE
        ).get(name=name, author=self.user)

        self.set_model_instance(note)

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

        if bool(instance):
            instance.update(**kwargs)
        else:
            note = Note.objects.create(author=self.user, **kwargs)
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
