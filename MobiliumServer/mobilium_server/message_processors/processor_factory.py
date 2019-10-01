from mobilium_proto_messages.message_processor import MessageProcessor
from mobilium_proto_messages.message_sender import MessageSender
from mobilium_server.message_processors.install_app_processor import InstallAppProcessor
from mobilium_server.message_processors.start_driver_processor import StartDriverProcessor
from mobilium_server.message_processors.uninstall_app_processor import UninstallAppProcessor
from mobilium_server.utils.shell_executor_pool import ShellExecutorPool


class ProcessorFactory:

    @staticmethod
    def make(message_sender: MessageSender, shell_executor_pool: ShellExecutorPool,
             address: str, port: int) -> MessageProcessor:
        uninstall_app_processor = UninstallAppProcessor(shell_executor_pool.new_executor(), message_sender)
        install_app_processor = InstallAppProcessor(shell_executor_pool.new_executor(), message_sender,
                                                    uninstall_app_processor)
        return StartDriverProcessor(shell_executor_pool.new_executor(), message_sender, address, port,
                                    install_app_processor)
