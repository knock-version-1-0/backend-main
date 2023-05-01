import faker, factory

from core.models import StatusChoice
from apps.notes.models import Note
from apps.users.models import User
from domains.constants import NOTE_NAME_LENGTH_LIMIT

fake = faker.Faker()

class NoteModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    author = User(1)
    name = factory.Sequence(lambda n: fake.unique.name()[:NOTE_NAME_LENGTH_LIMIT] if len(fake.unique.name()) > NOTE_NAME_LENGTH_LIMIT else fake.unique.name())
    status = StatusChoice.SAVE
