from typing import List
import faker

from domains.entities.users_entity import (
    UserEntity,
    AuthSessionEntity
)
from di.users_factory import UserFactory, AuthSessionFactory
from .utils import (
    get_unique_email,
    emailCode,
    timestamp
)

fake = faker.Faker()


def make_users(size=5) -> List[UserEntity]:
    repository = UserFactory().repository
    
    users = []
    for _ in range(size):
        users.append(repository.save(
            username=get_unique_email(),
            email=get_unique_email()
        ))

    return users


def make_auth_sessions(size=5) -> List[AuthSessionEntity]:
    factory = AuthSessionFactory()
    repository = factory.repository
    usecase = factory.usecase

    auth_sessions = []
    for _ in range(size):
        dto = usecase.generate_auth_session_data(get_unique_email(), timestamp)
        auth_sessions.append(repository.save(
            **dto.dict()
        ))
    
    return auth_sessions
