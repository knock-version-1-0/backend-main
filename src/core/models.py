from django.db import models

from django.utils.translation import gettext_lazy as _

# Create your models here.


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-created_at', '-updated_at']


class StatusChoice(models.IntegerChoices):
    SAVE = 1, _('저장됨')
    TEMP = 2, _('임시')
    EXPIRE = 3, _('만료')
    DELETE = 4, _('삭제')


StatusField = models.IntegerField(default=StatusChoice.TEMP, choices=StatusChoice.choices)
