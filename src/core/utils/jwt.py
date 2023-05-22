import jwt
from django.conf import settings

from core.utils.typing import ID, TokenData


def generate_jwt_token(id: ID, exp: int, at: int, type: str):
    """
    Generates a JSON Web Token that stores this user's ID and has an expiry
    date set to {EXPIRE_PERIOD} into the future.
    """
    data: TokenData = {
        'id': id,
        'exp': exp,
        'at': at,
        'token_type': type
    }

    token = jwt.encode(data, key=settings.SECRET_KEY, algorithm='HS256')

    return token


def parse_jwt_token(jwt_: str) -> TokenData:
    data: TokenData = jwt.decode(jwt_, settings.SECRET_KEY, algorithms=['HS256'])
    return data
