import pytest

from mixer.backend.django import mixer
from django.db.utils import IntegrityError

from apps.notes.models import (
    Note,
    Keyword,
)


@pytest.mark.django_db(transaction=True)
def test_note_name_integrity():
    """
    동일한 Author일 경우 Note.name을 중복해서 등록할 수 없습니다.
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


@pytest.mark.django_db(transaction=True)
def test_keyword_order_integrity():
    """
    Keyword.order는 Note내에서 중복을 허용하지 않습니다.
    """
    note1 = mixer.blend('notes.Note')
    note2 = mixer.blend('notes.Note')

    obj = Keyword.objects.create(note=note1, order=1)

    with pytest.raises(IntegrityError):
        obj = Keyword.objects.create(note=note1, order=1)

    obj = Keyword.objects.create(note=note2, order=1)


@pytest.mark.django_db
def test_keyword_order_by():
    """
    Keyword는 Keyword.order 별로 정렬됩니다.
    """
    note = mixer.blend('notes.Note')

    for i in range(10, 0, -1):
        Keyword.objects.create(
            note=note,
            order=i
        )
    
    keywords = Keyword.objects.filter(note=note)
    for i in range(10):
        assert keywords[i].order == i+1
