# pylint: disable=E0602, E0611, E0401, W0401
from typing import Optional, TypeVar, Type

from google.protobuf.message import Message
from mobilium_proto_messages.proto.messages_pb2 import *


class MessageDeserializer:
    T = TypeVar("T", bound=Message)  # pylint: disable=C0103

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
    def launch_app_response(data: bytes) -> Optional[LaunchAppResponse]:
        return MessageDeserializer.__message(data, LaunchAppResponse)

    @staticmethod
    def is_element_visible_response(data: bytes) -> Optional[IsElementVisibleResponse]:
        return MessageDeserializer.__message(data, IsElementVisibleResponse)

    @staticmethod
    def get_value_of_element_response(data: bytes) -> Optional[GetValueOfElementResponse]:
        return MessageDeserializer.__message(data, GetValueOfElementResponse)

    @staticmethod
    def click_element_response(data: bytes) -> Optional[ClickElementResponse]:
        return MessageDeserializer.__message(data, ClickElementResponse)

    @staticmethod
    def terminate_app_response(data: bytes) -> Optional[TerminateAppResponse]:
        return MessageDeserializer.__message(data, TerminateAppResponse)

    @staticmethod
    def __message(data: bytes, type_of_meesage: Type[T]) -> Optional[T]:
        mobilium_message: Message = MobiliumMessage().FromString(data)
        message = getattr(mobilium_message, mobilium_message.WhichOneof('message'))
        if isinstance(message, type_of_meesage):
            return message
        return None
