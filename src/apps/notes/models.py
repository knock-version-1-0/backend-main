import uuid

from django.db import models

from core.models import TimestampedModel, StatusField
from core.utils.typing import Empty


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
        ordering = ['-pk']
    
    def update(self, **kwargs):
        update_fields = []
        for key, value in kwargs.items():
            if value is not Empty:
                setattr(self, key, value)
                update_fields.append(key)
        self.save(update_fields=update_fields)
    
    def shared_only(self, user):
        if user.pk != self.author.pk:
            return False
        return True

    def author_only(self, user):
        if user.pk != self.author.pk:
            return False
        return True


class KeywordStatusChoice(models.IntegerChoices):
    UNSELECT = (1, 'UNSELECT')
    SELECT = (2, 'SELECT')
    EDIT = (3, 'EDIT')


class Keyword(models.Model):
    note = models.ForeignKey(Note, related_name='keywords', on_delete=models.CASCADE)
    parent = models.ForeignKey('Keyword', on_delete=models.CASCADE, null=True)
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()
    text = models.CharField(max_length=12, null=True, blank=True)
    status = models.IntegerField(choices=KeywordStatusChoice.choices)
    timestamp = models.CharField(max_length=13)

    class Meta:
        db_table = 'notes_keyword'


class KeywordChildren(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    child = models.ForeignKey(Keyword, related_name='children', on_delete=models.CASCADE)

    class Meta:
        db_table = 'notes_keyword_children'
