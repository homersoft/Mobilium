# pylint: disable=E0602, E0611, E0401, W0401
import re

from google.protobuf.message import Message
from mobilium_proto_messages.accessibility import Accessibility, AccessibilityById, AccessibilityByXpath
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
    def is_element_visible_request(accessibility: Accessibility, timeout: float = 0) -> bytes:
        message = IsElementVisibleRequest()
        message.element_indicator.CopyFrom(MessageDataFactory.__element_indicator(accessibility))
        message.timeout = timeout
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def get_element_value_request(accessibility: Accessibility) -> bytes:
        message = GetValueOfElementRequest()
        message.element_indicator.CopyFrom(MessageDataFactory.__element_indicator(accessibility))
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def set_element_text_request(accessibility: Accessibility, text: str, clears: bool = True):
        message = SetValueOfElementRequest()
        message.element_indicator.CopyFrom(MessageDataFactory.__element_indicator(accessibility))
        message.text.value = text
        message.text.clears = clears
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def set_position_request(accessibility: Accessibility, position: float):
        message = SetValueOfElementRequest()
        message.element_indicator.CopyFrom(MessageDataFactory.__element_indicator(accessibility))
        message.position = position
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def set_selection_request(accessibility: Accessibility, selection: bool):
        message = SetValueOfElementRequest()
        message.element_indicator.CopyFrom(MessageDataFactory.__element_indicator(accessibility))
        message.selection = selection
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def click_element_request(accessibility: Accessibility) -> bytes:
        message = ClickElementRequest()
        message.element_indicator.CopyFrom(MessageDataFactory.__element_indicator(accessibility))
        return MessageDataFactory.__data_with(message)

    @staticmethod
    def get_elements_count_request(accessibility: Accessibility, timeout: float = 0) -> bytes:
        message = GetElementsCountRequest()
        message.timeout = timeout
        message.element_indicator.CopyFrom(MessageDataFactory.__element_indicator(accessibility))
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

    @staticmethod
    def __element_indicator(accessibility: Accessibility) -> ElementIndicator:
        element_indicator = ElementIndicator()
        if isinstance(accessibility, AccessibilityById):
            element_indicator.id = accessibility.value
        elif isinstance(accessibility, AccessibilityByXpath):
            element_indicator.xpath = accessibility.value
        return element_indicator
