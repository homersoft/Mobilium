# pylint: disable=E0602, E0611, E0401, W0401
from google.protobuf.message import Message
from mobilium_proto_messages.proto.messages_pb2 import *


class MessageDataFactory:

    @staticmethod
    def start_driver_request() -> bytes:
        return MessageDataFactory.__data_with(StartDriverRequest())

    @staticmethod
    def execute_test_request() -> bytes:
        return MessageDataFactory.__data_with(ExecuteTestRequest())

    @staticmethod
    def install_app_request() -> bytes:
        return MessageDataFactory.__data_with(InstallAppRequest())

    @staticmethod
    def uninstall_app_request() -> bytes:
        return MessageDataFactory.__data_with(UninstallAppRequest())

    @staticmethod
    def install_app_response() -> bytes:
        return MessageDataFactory.__data_with(InstallAppResponse())

    @staticmethod
    def uninstall_app_response() -> bytes:
        return MessageDataFactory.__data_with(UninstallAppResponse())

    @staticmethod
    def __data_with(message: Message) -> bytes:
        class_name = message.__class__.__name__
        attribute_name = class_name[0].lower() + class_name[1:]
        mobilium_message = MobiliumMessage()
        getattr(mobilium_message, attribute_name).CopyFrom(message)
        return mobilium_message.SerializeToString()
