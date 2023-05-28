from typing import List
import faker, factory
from datetime import datetime

from core.models import StatusChoice
from domains.entities.users_entity import (
    UserEntity,
)
from di.users_factory import UserFactory

fake = faker.Faker()

email = 'user_name@email.com'
timestamp = int(datetime.now().strftime('%s'))


def make_users(size=5) -> List[UserEntity]:
    repository = UserFactory().repository
    
    users = []
    for _ in range(size):
        users.append(repository.save(
            username=email,
            email=email
        ))

    return users
