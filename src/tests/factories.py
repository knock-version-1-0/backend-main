import faker, factory

from core.models import StatusChoice
from apps.notes.models import Note
from apps.users.models import User

fake = faker.Faker()


class NoteModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    author = User(1)
    name = factory.LazyAttribute(lambda obj: fake.unique.name())
    status = StatusChoice.SAVE
