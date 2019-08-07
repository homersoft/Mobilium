from abc import ABC, abstractmethod
from typing import Optional

from MobiliumProtoMessages.mobilium_proto_messages.message_sender import MessageSender


class MessageProcessor(ABC):

    def __init__(self, message_sender: MessageSender, successor: Optional['MessageProcessor'] = None):
        self._next_processor = successor
        self.message_sender = message_sender

    @abstractmethod
    async def process(self, data: bytes):
        if self._next_processor:
            await self._next_processor.process(data)
