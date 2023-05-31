from django.db.utils import DatabaseError as _DatabaseError
from django.core.exceptions import ValidationError as _ValidationError
import jwt


class DatabaseError(_DatabaseError):
    error_type = _DatabaseError
    def __init__(self, e, *args):
        super().__init__(e, *args)


class ValidationError(_ValidationError):
    error_type = _ValidationError
    def __init__(self, e, *args):
        super().__init__(e, *args)


class ExpiredSignatureError(Exception):
    message = "Token is expired"
    error_type = jwt.exceptions.ExpiredSignatureError
    def __init__(self, *args):
        super().__init__(self.message, *args)
