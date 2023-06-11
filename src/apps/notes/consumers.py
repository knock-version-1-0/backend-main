from core.consumers import Consumer
from core.ws.request import Request
from core.ws.response import Response


APP_NAME = "notes"


class NoteUpdateKeywordConsumer(Consumer):
    app_name = APP_NAME
    key_name = "note_id"
    
    def update(self, request: Request):
        return self.controller.update(
            request=request,
            key=request.key
        )


class NoteCreateKeywordConsumer(Consumer):
    app_name = APP_NAME
    key_name = "note_id"

    def create(self, request: Request) -> Response:
        return self.controller.create(
            request=request
        )
