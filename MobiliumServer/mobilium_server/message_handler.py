class MessageHandler:
    def __init__(self, name: str):
        self.name = name
        self.broker = None

    def process_message(self, data: bytes):
        pass
