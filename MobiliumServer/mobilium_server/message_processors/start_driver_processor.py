from os import path
from typing import Optional

from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_proto_messages.message_sender import MessageSender
from mobilium_proto_messages.message_processor import MessageProcessor
from mobilium_server.utils.shell_executor import ShellExecutor
from mobilium_server.message_processors.shell_message_processor import ShellMessageProcessor


class StartDriverProcessor(ShellMessageProcessor):

    INTERNAL_PROJECT_DIR = '../MobiliumDriver/'
    EXTERNAL_PROJECT_DIR = 'mobilium/MobiliumDriver/'
    PROJECT_NAME = 'MobiliumDriver.xcodeproj'
    SCHEME = 'MobiliumDriver'

    def __init__(self, shell_executor: ShellExecutor, message_sender: MessageSender, address: str, port: int,
                 successor: Optional[MessageProcessor] = None):
        super().__init__(shell_executor, message_sender, successor)
        self.address = address
        self.port = port

    async def _process(self, data: bytes):
        message = MessageDeserializer.start_driver_request(data)
        if message is not None:
            self.start_driver(message.udid)

    def start_driver(self, udid: str):
        project_dir = self.project_dir()
        project_path = project_dir + self.PROJECT_NAME
        update_carthage_command = 'cd {} ; carthage update --platform iOS --cache-builds'.format(project_dir)
        self.shell_executor.execute(update_carthage_command, track_output=True)
        build_command = 'xcodebuild -project {0} -scheme {1} -destination "platform=iOS,id={2}" HOST={3} PORT={4} test'\
            .format(project_path, StartDriverProcessor.SCHEME, udid, self.address, self.port)
        self.shell_executor.execute(build_command, track_output=True, waits_for_termination=False)

    def project_dir(self):
        if path.exists(self.INTERNAL_PROJECT_DIR):
            return self.INTERNAL_PROJECT_DIR
        return self.EXTERNAL_PROJECT_DIR
