from mobilium_proto_messages.message_data_factory import MessageDataFactory
from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_proto_messages.message_processor import MessageProcessor
from mobilium_server.shell_executor import ShellExecutor


class InstallAppProcessor(MessageProcessor):

    IPA_PATH = './app.ipa'

    async def _process(self, data: bytes):
        message = MessageDeserializer.install_app_request(data)
        if message is not None:
            await self.install_app(message.udid)

    async def install_app(self, udid: str):
        command = 'ideviceinstaller -u {0} -i {1}'.format(udid, InstallAppProcessor.IPA_PATH)
        ShellExecutor.execute(command)
        message = MessageDataFactory.install_app_response()
        await self.message_sender.send(message)
