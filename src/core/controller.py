from core.service import BaseService


class BaseController:
    def __init__(self, service: BaseService):
        self.service = service

    def retrieve(self, request, key):
        raise NotImplementedError()

    def list(self, request):
        raise NotImplementedError()

    def create(self, request):
        raise NotImplementedError()

    def update(self, request, key):
        raise NotImplementedError()
