from mobilium_proto_messages.message_data_factory import MessageDataFactory
from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_server.message_processors.shell_message_processor import ShellMessageProcessor


class UninstallAppProcessor(ShellMessageProcessor):

    async def _process(self, data: bytes):
        message = MessageDeserializer.uninstall_app_request(data)
        if message is not None:
            await self.uninstall_app(message.udid, message.bundle_id)

    async def uninstall_app(self, udid: str, bundle_id: str):
        command = 'ideviceinstaller -u {0} -U {1}'.format(udid, bundle_id)
        self.shell_executor.execute(command)
        message = MessageDataFactory.uninstall_app_response()
        await self.message_sender.send(message)
