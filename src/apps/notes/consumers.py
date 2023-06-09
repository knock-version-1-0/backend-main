import json

from core.consumers import Consumer

APP_NAME = "notes"


class NoteUpdateKeywordConsumer(Consumer):
    app_name = APP_NAME
    key_name = "note_id"
    
    async def notes_message(self, event):
        message = event["message"]
        data = json.loads(message)

        await self.send(text_data=json.dumps({"status": 'OK', "data": data}))


class NoteCreateKeywordConsumer(Consumer):
    app_name = APP_NAME
    key_name = "note_id"

    async def notes_message(self, event):
        await self.send(text_data=self.controller.create(event))
