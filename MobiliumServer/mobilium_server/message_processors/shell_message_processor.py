from typing import Optional
from abc import abstractmethod

from mobilium_proto_messages.message_processor import MessageProcessor
from mobilium_server.shell_executor import ShellExecutor
from mobilium_proto_messages.message_sender import MessageSender


class ShellMessageProcessor(MessageProcessor):

    def __init__(self, shell_excecutor: ShellExecutor, message_sender: MessageSender,
                 successor: Optional['MessageProcessor'] = None):
        super().__init__(message_sender, successor)
        self.shell_executor = shell_excecutor

    @abstractmethod
    async def _process(self, data: bytes):
        pass
