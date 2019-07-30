# pylint: disable=undefined_variable, no_name_in_module, import_error, wildcard_import
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

    @staticmethod
    def install_app_request() -> bytes:
        message = MobiliumMessage()
        message.installAppRequest.CopyFrom(InstallAppRequest())
        return message.SerializeToString()

    @staticmethod
    def uninstall_app_request() -> bytes:
        message = MobiliumMessage()
        message.uninstallAppRequest.CopyFrom(UninstallAppRequest())
        return message.SerializeToString()

    @staticmethod
    def install_app_response() -> bytes:
        message = MobiliumMessage()
        message.installAppResponse.CopyFrom(InstallAppResponse())
        return message.SerializeToString()

    @staticmethod
    def uninstall_app_response() -> bytes:
        message = MobiliumMessage()
        message.uninstallAppResponse.CopyFrom(UninstallAppResponse())
        return message.SerializeToString()
