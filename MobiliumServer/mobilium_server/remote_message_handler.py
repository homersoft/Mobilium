# pylint: disable=W0613, W0233
from socketio import AsyncNamespace

from mobilium_server.message_handler import MessageHandler


class RemoteMessageHandler(MessageHandler, AsyncNamespace):

    def __init__(self, name: str):
        MessageHandler.__init__(self, name)
        AsyncNamespace.__init__(self, name)
        self.is_connected = None

    def on_connect(self, sid, environ):
        print('{0} connected'.format(self.name))
        self.is_connected = True

    def on_disconnect(self, sid):
        print('{0} disconnected'.format(self.name))
        self.is_connected = False

    async def process_message(self, data: bytes):
        print('{0} << {1}'.format(self.name, data))
        await self.send(data)

    async def on_message(self, sid, data: bytes):
        await self.broker.process_message(data)
