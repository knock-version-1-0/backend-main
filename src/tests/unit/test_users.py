import pytest

from domains.entities.users_entity import AuthToken
from apps.users.exceptions import InvalidTokenType


@pytest.mark.unit
def test_auth_token_type_validation():
    with pytest.raises(InvalidTokenType):
        AuthToken(type='other_type', value='adfsafewfvcz')

    token = AuthToken(type='refresh', value='asdfjwlejv')
    assert token.type == 'refresh'

    token = AuthToken(type='access', value='asdjfewvcx')
    assert token.type == 'access'
