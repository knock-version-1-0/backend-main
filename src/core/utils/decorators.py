from core.usecase import BaseUsecase


def authorize_required(func):
    def wrapper(self: BaseUsecase, *args, user_id=None, **kwargs):
        if user_id is None:
            raise ValueError('user_id required')
        self.repository.authorize(user_id=user_id)
        return func(self, *args, user_id=user_id, **kwargs)

    return wrapper
