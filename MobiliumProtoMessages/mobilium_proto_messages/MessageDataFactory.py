from mobilium_proto_messages.proto.messages_pb2 import *


class MessageDataFactory:

    @staticmethod
    def start_driver_request() -> bytes:
        message = MobiliumMessage()
        message.startDriverRequest.CopyFrom(StartDriverRequest())
        return message.SerializeToString()

    @staticmethod
    def execute_test_request() -> bytes:
        message = MobiliumMessage()
        message.executeTestRequest.CopyFrom(ExecuteTestRequest())
        return message.SerializeToString()
