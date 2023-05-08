import pytest
from apps.users.models import User


@pytest.fixture
def user_fixture() -> User:
    user = User.objects.create_user('fixture_user')
    return user
