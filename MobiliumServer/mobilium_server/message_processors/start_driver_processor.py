from typing import Optional

from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_proto_messages.message_sender import MessageSender
from mobilium_proto_messages.message_processor import MessageProcessor
from mobilium_server.utils.shell_executor import ShellExecutor
from mobilium_server.message_processors.shell_message_processor import ShellMessageProcessor
from mobilium_server.utils.mobilium_driver_localization import get_project_dir, PROJECT_NAME, SCHEME


class StartDriverProcessor(ShellMessageProcessor):

    def __init__(self, shell_executor: ShellExecutor, message_sender: MessageSender, address: str, port: int,
                 successor: Optional[MessageProcessor] = None):
        super().__init__(shell_executor, message_sender, successor)
        self.address = address
        self.port = port

    async def _process(self, data: bytes):
        message = MessageDeserializer.start_driver_request(data)
        if message is not None:
            await self.start_driver(message.udid)

    async def start_driver(self, udid: str):
        project_dir = get_project_dir()
        build_command = 'xcodebuild -project {0} -scheme {1} -destination "platform=iOS,id={2}" HOST={3} PORT={4} test'\
            .format(project_dir + PROJECT_NAME, SCHEME, udid, self.address, self.port)
        await self.shell_executor.execute(build_command, track_output=True, waits_for_termination=False)
