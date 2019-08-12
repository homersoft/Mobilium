from mobilium_proto_messages.message_data_factory import MessageDataFactory
from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_proto_messages.message_processor import MessageProcessor
from mobilium_server.shell_executor import ShellExecutor


class InstallAppProcessor(MessageProcessor):

    async def _process(self, data: bytes):
        message = MessageDeserializer.install_app_request(data)
        if message is not None:
            await self.install_app(message.udid, message.file_path)

    async def install_app(self, udid: str, file_path: str):
        command = 'ideviceinstaller -u {0} -i {1}'.format(udid, file_path)
        ShellExecutor.execute(command)
        message = MessageDataFactory.install_app_response()
        await self.message_sender.send(message)
