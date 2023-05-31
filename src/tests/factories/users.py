from typing import List
import faker, factory
from datetime import datetime

from core.models import StatusChoice
from domains.entities.users_entity import (
    UserEntity,
    AuthSessionEntity
)
from di.users_factory import UserFactory, AuthSessionFactory

fake = faker.Faker()

email = 'user_name@email.com'
timestamp = int(datetime.now().strftime('%s'))
emailCode = '000000'


def make_users(size=5) -> List[UserEntity]:
    repository = UserFactory().repository
    
    users = []
    for _ in range(size):
        users.append(repository.save(
            username=email,
            email=email
        ))

    return users


def make_auth_sessions(size=5) -> List[AuthSessionEntity]:
    factory = AuthSessionFactory()
    repository = factory.repository
    usecase = factory.usecase

    auth_sessions = []
    for _ in range(size):
        dto = usecase.generate_auth_session_data(email, timestamp)
        auth_sessions.append(repository.save(
            **dto.dict()
        ))
    
    return auth_sessions
