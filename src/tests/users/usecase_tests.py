import pytest
import uuid
from datetime import datetime, timedelta
from unittest.mock import Mock

from domains.usecases.users_usecase import AuthUsecase
from domains.entities.users_entity import (
    AuthSessionEntity,
    UserEntity
)
from apps.users.exceptions import (
    EmailSendFailed,
    AuthenticationFailed,
    AuthSessionDoesNotExist,
    AuthSessionExpired
)
from tests.fixtures.users import (
    email
)


@pytest.mark.unit
def test_auth_session_period_validation():
    """
    UseCase(USER1): AuthSession의 period는 5분 30초입니다.
    """
    assert AuthUsecase.get_auth_session_period() == timedelta(seconds=330)
    
    auth_session_data = AuthUsecase.generate_auth_session_data(
        email='user_name@email.com',
        at=int(datetime.now().strftime('%s'))
    )
    AuthUsecase.validate_auth_session_period(AuthSessionEntity(
        id=uuid.uuid4(),
        email=auth_session_data.email,
        emailCode=auth_session_data.emailCode,
        exp=auth_session_data.exp,
        at=auth_session_data.at,
        attempt=auth_session_data.attempt
    ))


@pytest.mark.unit
def test_email_transfer_validation():
    """
    UseCase(USER2): Email 전송이 성공적으로 이루었는지 여부를 검증해야 합니다.
    """
    with pytest.raises(EmailSendFailed):
        AuthUsecase.validate_email_transfer(0)
    
    AuthUsecase.validate_email_transfer(1)


@pytest.mark.unit
def test_email_code_input_validation():
    """
    UseCase(USER3): Email code를 잘못 입력하였는지 여부를 검증해야 합니다.
    """
    code = uuid.uuid4()
    auth_session = Mock(emailCode=code)
    auth_verification = Mock(emailCode=code)

    AuthUsecase.validate_email_code_input(auth_session, auth_verification)

    auth_verification = Mock(emailCode=uuid.uuid4())
    with pytest.raises(AuthenticationFailed):
        AuthUsecase.validate_email_code_input(auth_session, auth_verification)


@pytest.mark.unit
def test_session_data_email_validation():
    """
    UseCase(USER4): session id에 해당하는 session data 내의 email이 같은지 검증해야 합니다.
    """
    auth_session = Mock(email=email)
    auth_verification = Mock(email=email)

    AuthUsecase.validate_session_data_email(auth_session, auth_verification)

    auth_verification = Mock(email='other' + email)
    with pytest.raises(AuthSessionDoesNotExist):
        AuthUsecase.validate_session_data_email(auth_session, auth_verification)


@pytest.mark.unit
def test_session_data_expired():
    """
    UseCase(USER5): AuthSession의 기간이 만료되었는지 여부를 검증해야 합니다.
    """
    exp = int(datetime.now().strftime('%s'))
    auth_session = Mock(exp=exp)
    auth_verification = Mock(currentTime=exp-1)

    AuthUsecase.validate_session_expired(auth_session, auth_verification)

    auth_verification = Mock(currentTime=exp+1)
    with pytest.raises(AuthSessionExpired):
        AuthUsecase.validate_session_expired(auth_session, auth_verification)
