import json

from channels.generic.websocket import AsyncWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):
    app_name = None
    key_name = None

    async def connect(self):
        self.group_id = self.scope["url_route"]["kwargs"][self.key_name]
        self.group_name = f"{self.app_name}_{self.group_id}"

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.group_name, {"type": f"{self.app_name}_message", "message": message}
        )
