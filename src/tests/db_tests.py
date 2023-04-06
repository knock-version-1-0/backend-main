import pytest

from mixer.backend.django import mixer
from django.db.utils import IntegrityError

from apps.notes.models import Note


@pytest.mark.django_db(transaction=True)
def test_note_constraints():
    """
    Note name 관련 무결성 검사
    """
    author = mixer.blend('users.User')
    name = 'Test Note'
    note1 = Note.objects.create(author=author, name=name)
    
    # Test that creating a note with the same name and author raises an IntegrityError
    with pytest.raises(IntegrityError):
        note2 = Note.objects.create(author=author, name=name)

    # Test that creating a note with a different name and the same author does not raise an error
    note3 = Note.objects.create(author=author, name='Another Note')

    # Test that creating a note with the same name but a different author does not raise an error
    author2 = mixer.blend('users.User')
    note4 = Note.objects.create(author=author2, name=name)
