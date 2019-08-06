from abc import ABC, abstractmethod
from typing import Optional


class MessageProcessor(ABC):

    def __init__(self, successor: Optional['MessageProcessor'] = None):
        self._next_processor = successor

    @abstractmethod
    async def process(self, data: bytes):
        if self._next_processor:
            await self._next_processor.process(data)
