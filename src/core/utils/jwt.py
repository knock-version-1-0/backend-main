import jwt
from dataclasses import dataclass, asdict
from django.conf import settings


@dataclass
class TokenData:
    id: int
    exp: int
    at: int


def generate_jwt_token(_id: int, _exp: int, _at: int):
    """
    Generates a JSON Web Token that stores this user's ID and has an expiry
    date set to {EXPIRE_PERIOD} into the future.
    """
    data = TokenData(id=_id, exp=_exp, at=_at)

    token = jwt.encode(asdict(data), key=settings.SECRET_KEY, algorithm='HS256')

    return token


def parse_jwt_token(jwt_: str) -> dict:
    return jwt.decode(jwt_, settings.SECRET_KEY, algorithms=['HS256'])
