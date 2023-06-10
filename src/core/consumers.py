import json

from channels.generic.websocket import AsyncWebsocketConsumer
from core.controller import WsController
from core.ws.request import Request
from rest_framework.settings import api_settings


class BaseConsumer(AsyncWebsocketConsumer):
    app_name = None
    key_name = None

    def __init__(self, factory):
        self.factory = factory
        if self.groups is None:
            self.groups = []

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
        await self.channel_layer.group_send(
            self.group_name, {"type": "handle.message", "message": text_data}
        )
    
    async def handle_message(self, event):
        for method_name in self.get_crud_method_names():
            handler = getattr(self, method_name, None)
            if handler:
                request = self.get_request(event)
                self.initial(request)
                response = handler(request)
                await self.send(text_data=response.text_data)
                return
        raise Exception('CRUD method is not implemented.')


class Consumer(BaseConsumer):
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    __crud_method_names = ['create', 'list', 'retrieve', 'update', 'delete']
    
    def get_request(self, event) -> Request:
        message = event["message"]
        _json = json.loads(message)

        data = json.loads(_json['data'])
        authorization: str = _json.get('authorization')
        key = _json.get('key')

        request = Request(
            data=data,
            authorization=authorization,
            key=key,
            authenticators=self.get_authenticators()
        )

        return request
    
    def initial(self, request: Request):
        self.perform_authentication(request)
    
    def perform_authentication(self, request: Request):
        """
        Perform authentication on the incoming request.

        Note that if you override this and simply 'pass', then authentication
        will instead be performed lazily, the first time either
        `request.user` or `request.auth` is accessed.
        """
        request.user

    def get_authenticators(self):
        """
        Instantiates and returns the list of authenticators that this view can use.
        """
        return [auth() for auth in self.authentication_classes]
    
    def get_crud_method_names(self):
        return self.__crud_method_names

    @property
    def controller(self) -> WsController:
        return self.factory.controller
