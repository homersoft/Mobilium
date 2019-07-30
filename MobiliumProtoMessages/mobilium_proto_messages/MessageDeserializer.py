from typing import Optional, TypeVar, Type

from google.protobuf.message import Message
from mobilium_proto_messages.proto.messages_pb2 import *


class MessageDeserializer:
    T = TypeVar("T", bound=Message)

    @staticmethod
    def start_driver_request(data: bytes) -> Optional[StartDriverRequest]:
        return MessageDeserializer.__message(data, StartDriverRequest)

    @staticmethod
    def start_driver_response(data: bytes) -> Optional[StartDriverResponse]:
        return MessageDeserializer.__message(data, StartDriverResponse)

    @staticmethod
    def install_app_request(data: bytes) -> Optional[InstallAppRequest]:
        return MessageDeserializer.__message(data, InstallAppRequest)

    @staticmethod
    def install_app_response(data: bytes) -> Optional[InstallAppResponse]:
        return MessageDeserializer.__message(data, InstallAppResponse)

    @staticmethod
    def uninstall_app_request(data: bytes) -> Optional[UninstallAppRequest]:
        return MessageDeserializer.__message(data, UninstallAppRequest)

    @staticmethod
    def uninstall_app_response(data: bytes) -> Optional[UninstallAppResponse]:
        return MessageDeserializer.__message(data, UninstallAppResponse)

    @staticmethod
    def execute_test_response(data: bytes) -> Optional[ExecuteTestResponse]:
        return MessageDeserializer.__message(data, ExecuteTestResponse)

    @staticmethod
    def __message(data: bytes, type_of_meesage: Type[T]) -> Optional[T]:
        mobilium_message: Message = MobiliumMessage().FromString(data)
        message = getattr(mobilium_message, mobilium_message.WhichOneof('message'))
        if isinstance(message, type_of_meesage):
            return message
        return None
