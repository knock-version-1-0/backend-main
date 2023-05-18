from core.utils.pydantic import RequestBody


class AuthSessionDto(RequestBody):
    id: str
    email: str
    emailCode: str
    currentDate: int

    def dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'email_code': self.emailCode,
            'current_date': self.currentDate
        }
