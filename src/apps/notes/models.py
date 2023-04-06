import uuid

from django.db import models

from core.models import TimestampedModel, StatusField


class Note(TimestampedModel):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    display_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    status = StatusField

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

    class Meta:
        db_table = 'notes_keyword'


class Position(models.Model):
    keyword = models.ForeignKey(Keyword, related_name='positions', on_delete=models.CASCADE)
    order = models.IntegerField(unique=True)

    class Meta:
        db_table = 'notes_position'
        constraints = [
            models.UniqueConstraint(fields=['order', 'keyword'], name='keyword_position_order_integrity')
        ]
        ordering = ['order',]
