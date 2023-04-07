import uuid

from django.db import models, transaction
from django.db.utils import IntegrityError

from core.models import TimestampedModel, StatusField


class NoteManager(models.Manager):
    def create(self, author, keywords, **kwargs):
        with transaction.atomic():
            try:
                note = super().create(
                    author=author,
                    **kwargs
                )
            except IntegrityError:
                raise IntegrityError('note_integrity_error')
            
            try:
                keywords = [Keyword.objects.create(
                    note=note,
                    pos_id=k['posId']
                ) for k in keywords]
            except IntegrityError:
                raise IntegrityError('keyword_integrity_error')

        return note


class Note(TimestampedModel):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    display_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    status = StatusField

    objects = NoteManager()

    class Meta:
        db_table = 'notes_note'
        constraints = [
            models.UniqueConstraint(fields=['name', 'author'], name='note_name_integrity')
        ]
        indexes = [
            models.Index(fields=['name', 'author'])
        ]
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save(update_fields=kwargs.keys())


class Keyword(models.Model):
    note = models.ForeignKey(Note, related_name='keywords', on_delete=models.CASCADE)
    pos_id = models.IntegerField()

    class Meta:
        db_table = 'notes_keyword'
        ordering = ['pos_id',]
        constraints = [
            models.UniqueConstraint(fields=['pos_id', 'note'], name='keyword_pos_id_integrity')
        ]
