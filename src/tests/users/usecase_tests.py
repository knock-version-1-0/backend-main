import pytest
from datetime import datetime

from domains.usecases.users_usecase import AuthUseCase


@pytest.mark.unit
def test_auth_session_period_validation():
    auth_session = AuthUseCase.generate_auth_session(
        email='user_name@email.com',
        at=int(datetime.now().strftime('%s'))
    )
    AuthUseCase.validate_auth_session_period(auth_session)
