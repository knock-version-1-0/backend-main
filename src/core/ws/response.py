class Response:
    def __init__(self, data=None, status=None, exception=False):
        self.data = data
        self._status = status
        self.exception = exception
