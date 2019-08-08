from abc import ABC, abstractmethod
from typing import Optional

from mobilium_proto_messages.message_sender import MessageSender


class MessageProcessor(ABC):

    def __init__(self, message_sender: MessageSender, successor: Optional['MessageProcessor'] = None):
        self._next_processor = successor
        self.message_sender = message_sender

    async def process(self, data: bytes):
        await self._process(data)
        if self._next_processor:
            await self._next_processor.process(data)

    @abstractmethod
    async def _process(self, data: bytes):
        pass
