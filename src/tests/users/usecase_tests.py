import pytest
from datetime import datetime, timedelta

from domains.usecases.users_usecase import AuthUseCase


@pytest.mark.unit
def test_auth_session_period_validation():
    """
    UseCase(USER1): AuthSession의 period는 5분 30초입니다.
    """
    assert AuthUseCase.get_auth_session_period() == timedelta(seconds=330)
    
    auth_session = AuthUseCase.generate_auth_session(
        email='user_name@email.com',
        at=int(datetime.now().strftime('%s'))
    )
    AuthUseCase.validate_auth_session_period(auth_session)
