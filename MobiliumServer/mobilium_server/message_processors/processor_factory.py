from mobilium_proto_messages.message_processor import MessageProcessor
from mobilium_proto_messages.message_sender import MessageSender
from mobilium_server.message_processors.install_app_processor import InstallAppProcessor
from mobilium_server.message_processors.start_driver_processor import StartDriverProcessor
from mobilium_server.message_processors.uninstall_app_processor import UninstallAppProcessor


class ProcessorFactory:

    @staticmethod
    def make(message_sender: MessageSender, address: str, port: int) -> MessageProcessor:
        uninstall_app_processor = UninstallAppProcessor(message_sender)
        install_app_processor = InstallAppProcessor(message_sender, uninstall_app_processor)
        return StartDriverProcessor(message_sender, address, port, install_app_processor)
