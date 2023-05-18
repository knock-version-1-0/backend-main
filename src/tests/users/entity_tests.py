import pytest
import uuid
from datetime import timedelta, datetime

from domains.entities.users_entity import (
    UserEntity,
    AuthSessionEntity,
)
from tests.fixtures.users import (
    user_entity_fixture,
)
from core.utils.jwt import parse_jwt_token, TokenData
from apps.users.exceptions import (
    AuthTokenCannotRead,
    AttemptLimitOver
)


@pytest.mark.unit
def test_user_entity(user_entity_fixture):
    user: UserEntity = user_entity_fixture

    assert isinstance(user.id, int)
    assert isinstance(user.username, str)
    assert isinstance(user.email, str)
    assert isinstance(user.isActive, bool)
    assert isinstance(user.isStaff, bool)


@pytest.mark.unit
def test_user_token(user_entity_fixture):
    """
    User에서 accessToken과 refreshToken을 생성할 수 있습니다.
    """

    user_entity: UserEntity = user_entity_fixture

    refresh_token = user_entity.refreshToken
    access_token = user_entity.accessToken

    refresh_token_data = TokenData(**parse_jwt_token(refresh_token.value))
    access_token_data = TokenData(**parse_jwt_token(access_token.value))
    
    # User.refreshToken의 만료 기간은 7일입니다.
    assert refresh_token.type == 'refresh'
    assert refresh_token_data.exp - refresh_token_data.at == int(timedelta(days=7).total_seconds())

    # User.accessToken의 만료 기간은 60분입니다.
    assert access_token.type == 'access'
    assert access_token_data.exp - access_token_data.at == int(timedelta(minutes=60).total_seconds())

    user_entity = user_entity.copy(update={'isActive': False})

    # User는 isActive 상태일 때, token을 생성할 수 있습니다.
    with pytest.raises(AuthTokenCannotRead):
        _ = user_entity.refreshToken
    with pytest.raises(AuthTokenCannotRead):
        _ = user_entity.accessToken


@pytest.mark.unit
def test_code_input_attempt_limit():
    """
    attempt는 최대 3회까지 가능합니다.
    """
    max_attempt = 3
    _now = datetime.now()
    session = AuthSessionEntity(
        id=uuid.uuid4(),
        email='user_name@email.com',
        emailCode='602617',
        exp=int((_now + timedelta(seconds=330)).strftime('%s')),
        at=int(_now.strftime('%s')),
        attempt=max_attempt
    )

    with pytest.raises(AttemptLimitOver):
        _dt = session.dict()
        _dt.pop('attempt')
        _ = AuthSessionEntity(**_dt, attempt=max_attempt+1)
