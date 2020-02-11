from mobilium_server.message_processors.shell_message_processor import ShellMessageProcessor
from mobilium_server.utils.mobilium_driver_localization import get_project_dir
from mobilium_proto_messages.message_data_factory import MessageDataFactory
from mobilium_proto_messages.message_deserializer import MessageDeserializer


class PrepareDriverProcessor(ShellMessageProcessor):

    async def _process(self, data: bytes):
        message = MessageDeserializer.prepare_driver_request(data)
        if message is not None:
            await self.prepare_driver()

    async def prepare_driver(self):
        project_dir = get_project_dir()
        update_carthage_command = 'cd {} ; carthage update --platform iOS --cache-builds ; cd -'.format(project_dir)
        await self.shell_executor.execute(update_carthage_command, track_output=True)

        message = MessageDataFactory.prepare_driver_response()
        await self.message_sender.send(message)
