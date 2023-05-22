import pytest
import uuid
from datetime import datetime, timedelta

from domains.usecases.users_usecase import AuthUseCase
from domains.entities.users_entity import AuthSessionEntity


@pytest.mark.unit
def test_auth_session_period_validation():
    """
    UseCase(USER1): AuthSession의 period는 5분 30초입니다.
    """
    assert AuthUseCase.get_auth_session_period() == timedelta(seconds=330)
    
    auth_session_data = AuthUseCase.generate_auth_session_data(
        email='user_name@email.com',
        at=int(datetime.now().strftime('%s'))
    )
    AuthUseCase.validate_auth_session_period(AuthSessionEntity(
        id=uuid.uuid4(),
        email=auth_session_data.email,
        emailCode=auth_session_data.emailCode,
        exp=auth_session_data.exp,
        at=auth_session_data.at,
        attempt=auth_session_data.attempt
    ))
