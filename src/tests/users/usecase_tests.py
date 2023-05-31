import pytest
import uuid
from datetime import datetime, timedelta
from unittest.mock import Mock

from domains.usecases.users_usecase import AuthSessionUsecase, AuthTokenUsecase
from domains.entities.users_entity import (
    AuthSessionEntity,
)
from apps.users.exceptions import (
    EmailSendFailed,
    AuthenticationFailed,
    AuthSessionDoesNotExist,
    AuthSessionExpired,
    RefreshTokenExpired,
    RefreshTokenRequired
)
from tests.fixtures.users import (
    email,
    user_entity_fixture
)
from di.users_factory import AuthTokenFactory
from core.utils.jwt import generate_jwt_token, parse_jwt_token
from adapters.dto.users_dto import AuthTokenDto


@pytest.mark.unit
def test_email_transfer_validation():
    """
    UseCase(USER2): Email 전송이 성공적으로 이루었는지 여부를 검증해야 합니다.
    """
    with pytest.raises(EmailSendFailed):
        AuthSessionUsecase.validate_email_transfer(0)
    
    AuthSessionUsecase.validate_email_transfer(1)


@pytest.mark.unit
def test_email_code_input_validation():
    """
    UseCase(USER3): Email code를 잘못 입력하였는지 여부를 검증해야 합니다.
    """
    code = uuid.uuid4()
    auth_session = Mock(emailCode=code)
    auth_verification = Mock(emailCode=code)

    AuthSessionUsecase.validate_email_code_input(auth_session, auth_verification)

    auth_verification = Mock(emailCode=uuid.uuid4())
    with pytest.raises(AuthenticationFailed):
        AuthSessionUsecase.validate_email_code_input(auth_session, auth_verification)


@pytest.mark.unit
def test_session_data_email_validation():
    """
    UseCase(USER4): session id에 해당하는 session data 내의 email이 같은지 검증해야 합니다.
    """
    auth_session = Mock(email=email)
    auth_verification = Mock(email=email)

    AuthSessionUsecase.validate_session_data_email(auth_session, auth_verification)

    auth_verification = Mock(email='other' + email)
    with pytest.raises(AuthSessionDoesNotExist):
        AuthSessionUsecase.validate_session_data_email(auth_session, auth_verification)


@pytest.mark.unit
def test_session_data_expired():
    """
    UseCase(USER5): AuthSession의 기간이 만료되었는지 여부를 검증해야 합니다.
    """
    exp = int(datetime.now().strftime('%s'))
    auth_session = Mock(exp=exp)
    auth_verification = Mock(currentTime=exp-1)

    AuthSessionUsecase.validate_session_expired(auth_session, auth_verification)

    auth_verification = Mock(currentTime=exp+1)
    with pytest.raises(AuthSessionExpired):
        AuthSessionUsecase.validate_session_expired(auth_session, auth_verification)


@pytest.mark.unit
def test_refresh_token_expired(user_entity_fixture):
    """
    UseCase(USER6): refreshToken의 만료 여부를 검증해야 합니다.
    """
    refresh_token = user_entity_fixture.refreshToken.value
    token_data = parse_jwt_token(refresh_token)
    token_data['exp'] = int(datetime.now().strftime('%s')) - 1000
    refresh_token = generate_jwt_token(
        id=token_data['id'],
        exp=token_data['exp'],
        at=token_data['at'],
        type=token_data['token_type']
    )
    with pytest.raises(RefreshTokenExpired):
        usecase = AuthTokenFactory().usecase
        usecase.create(dto=AuthTokenDto(type='refresh', value=refresh_token), max_age=1800)


@pytest.mark.unit
def test_refresh_token_type_required(user_entity_fixture):
    """
    UseCase(USER7): refreshToken type을 전달하였는지 여부를 검증해야 합니다.
    """
    refresh_token = user_entity_fixture.refreshToken.value
    with pytest.raises(RefreshTokenRequired):
        AuthTokenUsecase.validate_refresh_token_type(AuthTokenDto(
            type='other',
            value=refresh_token
        ))
