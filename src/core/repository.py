from typing import Optional

from django.contrib.auth import get_user_model
from domains.exceptions import UserInvalidError


class BaseRepository:
    def __init__(self, context: Optional[dict]=None, **kwargs): ...

    def find_all(self, *args, **kwargs): ...

    def find_by_id(self, id, *args, **kwargs): ...

    def save(self, entity: object, *args, **kwargs): ...

    def get_model_instance(self):
        try:
            return self.__model_instance
        except AttributeError:
            return None
    
    def set_model_instance(self, model):
        self.__model_instance = model

    def authorize(self, user_id):
        User = get_user_model()
        try:
            self.user = User.objects.filter(is_active=True).get(pk=user_id)
        except User.DoesNotExist:
            raise UserInvalidError()
