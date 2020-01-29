from functools import partial

from mobilium_server.message_handler import MessageHandler
from mobilium_server.remote_message_handler import RemoteMessageHandler
from mobilium_server.utils.wait import wait_until_true


class MessageBroker:
    def __init__(self):
        self.message_handlers: [MessageHandler] = []

    def register_message_handler(self, message_handler: MessageHandler):
        message_handler.broker = self
        self.message_handlers.append(message_handler)

    def unregister_message_handler(self, message_handler: MessageHandler):
        message_handler.broker = None
        self.message_handlers.remove(message_handler)

    async def process_message(self, data: bytes):
        print('>> {0}'.format(data))
        for handler in self.message_handlers:
            if hasattr(handler, "is_connected") and handler.is_connected is False:
                await self.__wait_until_connected(handler)
            await handler.process_message(data)

    async def __wait_until_connected(self, handler: RemoteMessageHandler):
        handler_name = handler.name
        print("{} waiting for connection...".format(handler_name))
        is_handler_connected = partial(self.__is_handler_connected, handler)
        timeout_message = "Reconnection failed for: {}".format(handler_name)
        await wait_until_true(is_handler_connected, timeout_message=timeout_message)
        print("{} reconnected".format(handler_name))

    @staticmethod
    def __is_handler_connected(handler: RemoteMessageHandler) -> bool:
        return handler.is_connected
