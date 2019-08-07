from mobilium_proto_messages.message_data_factory import MessageDataFactory
from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_proto_messages.message_processor import MessageProcessor
from mobilium_server.shell_executor import ShellExecutor


class UninstallAppProcessor(MessageProcessor):

    bundle_id = 'com.silvair.commissioning.test.dev'

    async def process(self, data: bytes):
        message = MessageDeserializer.uninstall_app_request(data)
        if message is not None:
            await self.uninstall_app(message.udid)
        await super(UninstallAppProcessor, self).process(data)

    async def uninstall_app(self, udid: str):
        command = 'ideviceinstaller -u {0} -U {1}'.format(udid, self.bundle_id)
        ShellExecutor.execute(command)
        message = MessageDataFactory.uninstall_app_response()
        await self.message_sender.send(message)