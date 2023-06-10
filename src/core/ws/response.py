import json


class Response:
    def __init__(self, data=None, status=None):
        self._data = data
        self._status = status
    
    @property
    def text_data(self):
        return json.dumps(self._data)
