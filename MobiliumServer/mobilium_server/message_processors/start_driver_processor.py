from typing import Optional

from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_proto_messages.message_processor import MessageProcessor
from mobilium_proto_messages.message_sender import MessageSender
from mobilium_server.shell_executor import ShellExecutor


class StartDriverProcessor(MessageProcessor):

    PROJECT = '../MobiliumDriver/MobiliumDriver.xcodeproj'
    SCHEME = 'MobiliumDriver'

    def __init__(self, message_sender: MessageSender, address: str, port: int,
                 successor: Optional[MessageProcessor] = None):
        super().__init__(message_sender, successor)
        self.address = address
        self.port = port
        self.shell_executor = ShellExecutor()

    async def _process(self, data: bytes):
        message = MessageDeserializer.start_driver_request(data)
        if message is not None:
            self.start_driver(message.udid)

    def start_driver(self, udid: str):
        command = 'xcodebuild -project {0} -scheme {1} -destination "platform=iOS,id={2}" HOST={3} PORT={4} test' \
            .format(StartDriverProcessor.PROJECT, StartDriverProcessor.SCHEME, udid, self.address, self.port)
        self.shell_executor.execute(command, track_output=True, waits_for_termination=False)
