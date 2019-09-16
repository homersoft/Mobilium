# pylint: disable=E0602, E0611, E0401, W0401
import re

from google.protobuf.message import Message
from mobilium_proto_messages.proto.messages_pb2 import *


class MessageDataFactory:

    @staticmethod
    def start_driver_request(udid: str) -> bytes:
        message = StartDriverRequest()
        message.udid = udid
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def launch_app_request(bundle_id: str) -> bytes:
        message = LaunchAppRequest()
        message.bundle_id = bundle_id
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def install_app_request(udid: str, file_path: str) -> bytes:
        message = InstallAppRequest()
        message.udid = udid
        message.file_path = file_path
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def uninstall_app_request(udid: str, bundle_id: str) -> bytes:
        message = UninstallAppRequest()
        message.udid = udid
        message.bundle_id = bundle_id
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def terminate_app_request() -> bytes:
        message = TerminateAppRequest()
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def install_app_response() -> bytes:
        return MessageDataFactory.__data_with(InstallAppResponse())

    @staticmethod
    def uninstall_app_response() -> bytes:
        return MessageDataFactory.__data_with(UninstallAppResponse())

    @staticmethod
    def is_element_visible_request(accessibility_id: str, timeout: float = 0) -> bytes:
        message = IsElementVisibleRequest()
        message.accessibility_id = accessibility_id
        message.timeout = timeout
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def get_value_of_element_request(accessibility_id: str) -> bytes:
        message = GetValueOfElementRequest()
        message.accessibility_id = accessibility_id
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def set_text_of_element_request(accessibility_id: str, text: str, clears: bool = True):
        message = SetValueOfElementRequest()
        message.accessibility_id = accessibility_id
        message.text.value = text
        message.text.clears = clears
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def set_position_of_slider_request(accessibility_id: str, position: float):
        message = SetValueOfElementRequest()
        message.accessibility_id = accessibility_id
        message.position = position
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def set_selection_of_checkbox_request(accessibility_id: str, selection: bool):
        message = SetValueOfElementRequest()
        message.accessibility_id = accessibility_id
        message.selection = selection
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def hide_keyboard_request() -> bytes:
        message = HideKeyboardRequest()
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def click_element_request(accessibility_id: str) -> bytes:
        message = ClickElementRequest()
        message.accessibility_id = accessibility_id
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def __data_with(message: Message) -> bytes:
        class_name = message.__class__.__name__
        attribute_name = '_'.join(MessageDataFactory.__camel_case_split(class_name)).lower()
        mobilium_message = MobiliumMessage()
        getattr(mobilium_message, attribute_name).CopyFrom(message)
        return mobilium_message.SerializeToString()

    @staticmethod
    def __camel_case_split(text: str) -> [str]:
        return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', text)
