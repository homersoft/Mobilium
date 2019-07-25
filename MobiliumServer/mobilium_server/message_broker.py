from mobilium_server.message_handler import MessageHandler


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
        for handler in self.message_handlers:
            await handler.process_message(data)
