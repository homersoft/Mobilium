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

    async def process_message(self, message: str):
        if message in ['DriverStarted', 'TestExecuted']:
            handler = next(handler for handler in self.message_handlers if handler.name == '/client')
            await handler.process_message(message)
        if message in ['ExecuteTest']:
            handler = next(handler for handler in self.message_handlers if handler.name == '/driver')
            await handler.process_message(message)
        if message in ['StartDriver']:
            handler = next(handler for handler in self.message_handlers if handler.name == 'server')
            await handler.process_message(message)
