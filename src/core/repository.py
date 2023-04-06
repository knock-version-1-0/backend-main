from django.contrib.auth import get_user_model


class BaseRepository:
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
        self.user = get_user_model().objects.get(pk=user_id)
