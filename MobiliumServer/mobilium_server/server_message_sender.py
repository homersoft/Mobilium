from mobilium_proto_messages.message_sender import MessageSender
from mobilium_server.server import Server


class ServerMessageSender(MessageSender):

    def __init__(self, server: Server):
        super().__init__()
        self.server = server

    async def send(self, data: bytes):
        await self.server.send_message(data)
