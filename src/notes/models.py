import uuid

from django.db import models

from core.models import TimestampedModel, StatusField


class Note(TimestampedModel):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    display_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=25)
    status = StatusField


    class Meta:
        db_table = 'notes_note'
        constraints = [
            models.UniqueConstraint(fields=['name', 'author'], name='unique_note_name_author')
        ]
