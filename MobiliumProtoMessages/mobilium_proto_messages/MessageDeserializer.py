from typing import Optional, TypeVar, Type

from google.protobuf.message import Message
from mobilium_proto_messages.proto.messages_pb2 import *


class MessageDeserializer:
    T = TypeVar("T", bound=Message)

    @staticmethod
    def start_driver_request(data: bytes) -> Optional[StartDriverRequest]:
        return MessageDeserializer.__message(data, StartDriverRequest)


    @staticmethod
    def __message(data: bytes, type_of_meesage: Type[T]) -> Optional[T]:
        mobilium_message: Message = MobiliumMessage().FromString(data)
        message = getattr(mobilium_message, mobilium_message.WhichOneof('message'))
        if type(message) is type_of_meesage:
            return message
        else:
            return None
