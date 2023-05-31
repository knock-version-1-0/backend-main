import pytest
import uuid
from datetime import timedelta, datetime

from domains.entities.users_entity import (
    UserEntity,
    AuthSessionEntity,
    AuthTokenEntity
)
from tests.fixtures.users import (
    user_entity_fixture,
    auth_session_entity_fixture,
    refresh_token_entity_fixture,
    access_token_entity_fixture
)
from core.utils.jwt import parse_jwt_token
from apps.users.exceptions import (
    AuthTokenCannotRead,
    AttemptLimitOver,
    InvalidTokenType,
)


@pytest.mark.unit
def test_user_entity(user_entity_fixture):
    """ yaml
    User:
        id: integer
        username: string
        isActive: boolean
        isStaff: boolean
        email: string
    """
    user: UserEntity = user_entity_fixture

    assert isinstance(user.id, int)
    assert isinstance(user.username, str)
    assert isinstance(user.email, str)
    assert isinstance(user.isActive, bool)
    assert isinstance(user.isStaff, bool)


@pytest.mark.unit
def test_auth_session_entity(auth_session_entity_fixture):
    """ yaml
    AuthSession:
        id: string
        emailCode: string
        exp: integer
        at: integer
        email: string
        attempt: integer
    """
    auth_session: AuthSessionEntity = auth_session_entity_fixture

    assert isinstance(auth_session.id, str)
    assert isinstance(auth_session.emailCode, str)
    assert isinstance(auth_session.exp, int)
    assert isinstance(auth_session.at, int)
    assert isinstance(auth_session.email, str)
    assert isinstance(auth_session.attempt, int)


@pytest.mark.unit
def test_auth_token_entity(refresh_token_entity_fixture, access_token_entity_fixture):
    """ yaml
    AuthToken:
        type:
            - 'refresh'
            - 'access'
        value: string
    """
    refresh_token: AuthTokenEntity = refresh_token_entity_fixture
    access_token: AuthTokenEntity = access_token_entity_fixture

    assert refresh_token.type == 'refresh'
    assert access_token.type == 'access'
    assert isinstance(refresh_token.value, str)


@pytest.mark.unit
def test_user_tokens(user_entity_fixture):
    """
    Entity(USER2): User에서 accessToken과 refreshToken을 생성할 수 있습니다.
    """

    user_entity: UserEntity = user_entity_fixture

    refresh_token= user_entity.refreshToken
    access_token = user_entity.accessToken

    refresh_token_data = parse_jwt_token(refresh_token.value)
    access_token_data = parse_jwt_token(access_token.value)

    assert refresh_token.type == 'refresh'
    assert refresh_token_data['token_type'] == 'refresh'

    assert access_token.type == 'access'
    assert access_token_data['token_type'] == 'access'


@pytest.mark.unit
def test_refresh_token_period(user_entity_fixture):
    """
    Entity(USER3): User.refreshToken의 만료 기간은 7일입니다.
    """
    user_entity: UserEntity = user_entity_fixture

    refresh_token = user_entity.refreshToken
    refresh_token_data = parse_jwt_token(refresh_token.value)

    assert refresh_token_data['exp'] - refresh_token_data['at'] == int(timedelta(days=7).total_seconds())


@pytest.mark.unit
def test_access_token_period(user_entity_fixture):
    """
    Entity(USER4): User.accessToken의 만료 기간은 60분입니다.
    """
    user_entity: UserEntity = user_entity_fixture

    access_token = user_entity.accessToken
    access_token_data = parse_jwt_token(access_token.value)

    assert access_token_data['exp'] - access_token_data['at'] == int(timedelta(minutes=60).total_seconds())


@pytest.mark.unit
def test_user_not_generate_token_when_inactive(user_entity_fixture):
    """
    Entity(USER1): User는 isActive 상태일 때, token을 생성할 수 있습니다.
    """

    user_entity: UserEntity = user_entity_fixture
    user_entity = user_entity.copy(update={'isActive': False})

    with pytest.raises(AuthTokenCannotRead):
        _ = user_entity.refreshToken
    with pytest.raises(AuthTokenCannotRead):
        _ = user_entity.accessToken


@pytest.mark.unit
def test_code_input_attempt_limit():
    """
    Entity(USER5): attempt는 최대 3회까지 가능합니다.
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


@pytest.mark.unit
def test_auth_token_type_validation():
    """
    Entity(USER6): AuthToken의 type은 ‘refresh’와 ‘access’만 입력 가능합니다.
    """
    with pytest.raises(InvalidTokenType):
        AuthTokenEntity(type='other_type', value='adfsafewfvcz')

    token = AuthTokenEntity(type='refresh', value='asdfjwlejv')
    assert token.type == 'refresh'

    token = AuthTokenEntity(type='access', value='asdjfewvcx')
    assert token.type == 'access'


@pytest.mark.unit
def test_auth_session_expire_period():
    """
    Entity(USER7): AuthSession의 만료기간은 330초 입니다.
    """
    assert int(AuthSessionEntity.get_expire_period().total_seconds()) == 330
