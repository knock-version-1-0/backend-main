from .auth import *
from .notes import *

from django.db.utils import DatabaseError as _DatabaseError


class DatabaseError(_DatabaseError):
    error_type = _DatabaseError
    def __init__(self, e, *args):
        super().__init__(e, *args)
