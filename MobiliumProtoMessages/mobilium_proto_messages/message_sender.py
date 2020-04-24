from abc import ABC, abstractmethod


class MessageSender(ABC):

    @abstractmethod
    async def send(self, data: bytes):
        pass
