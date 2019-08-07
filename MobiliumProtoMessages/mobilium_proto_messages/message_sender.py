from abc import ABC, abstractmethod


class MessageSender(ABC):

    def __init__(self):
        pass

    @abstractmethod
    async def send(self, data: bytes):
        pass
