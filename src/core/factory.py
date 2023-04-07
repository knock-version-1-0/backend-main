class BaseFactory:
    @property
    def repository(self):
        raise NotImplementedError()
    @property
    def usecase(self):
        raise NotImplementedError()
    @property
    def service(self):
        raise NotImplementedError()
    @property
    def controller(self):
        raise NotImplementedError()
