from core.utils.pydantic import RequestBody


class AuthSessionDto(RequestBody):
    email: str
    emailCode: str
    exp: int
    at: int
    attempt: int

    def dict(self) -> dict:
        return {
            'email': self.email,
            'email_code': self.emailCode,
            'exp': str(self.exp),
            'at': str(self.at),
            'attempt': self.attempt
        }


class AuthTokenDto(RequestBody):
    type: str
    value: str


class AuthVerificationDto(RequestBody):
    id: str
    email: str
    emailCode: str
    currentTime: int

    def dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'email_code': self.emailCode,
            'current_time': self.currentTime
        }


class AuthEmailDto(RequestBody):
    email: str
    at: int


class UserDto(RequestBody):
    email: str
