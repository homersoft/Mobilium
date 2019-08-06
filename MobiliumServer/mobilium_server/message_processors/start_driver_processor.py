from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_proto_messages.message_processor import MessageProcessor
from mobilium_server.shell_executor import ShellExecutor


class StartDriverProcessor(MessageProcessor):

    def __init__(self, address: str, port: int):
        super().__init__()
        self.address = address
        self.port = port

    async def process(self, data: bytes):
        message = MessageDeserializer.start_driver_request(data)
        if message is not None:
            self.start_driver(message.udid)
            return True

    def start_driver(self, udid: str):
        project = '../MobiliumDriver/MobiliumDriver.xcodeproj'
        scheme = 'MobiliumDriver'
        command = 'xcodebuild -project {0} -scheme {1} -destination "platform=iOS,id={2}" HOST={3} PORT={4} test' \
            .format(project, scheme, udid, self.address, self.port)
        ShellExecutor.execute(command, waits_for_termination=False)
