from socketio import AsyncNamespace

from mobilium_server.message_handler import MessageHandler


class RemoteMessageHandler(MessageHandler, AsyncNamespace):
    def __init__(self, name: str):
        MessageHandler.__init__(self, name)
        AsyncNamespace.__init__(self, name)

    def on_connect(self, sid, environ):
        print('{0} connected'.format(self.name))

    def on_disconnect(self, sid):
        print('{0} disconnected'.format(self.name))

    async def process_message(self, message: str):
        print('{0} << {1}'.format(self.name, message))
        await self.send(message)

    async def on_message(self, sid, data: bytes):
        await self.broker.process_message(data)
