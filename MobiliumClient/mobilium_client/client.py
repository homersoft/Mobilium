# pylint: disable=E0611, E0401
import argparse
import time
from typing import Optional, Callable, TypeVar
from common.named_partial import named_partial
from common.wait import wait_until_true, wait_until_value
from common.exceptions import ElementNotFoundException
from mobilium_client import config
from mobilium_client.client_namespace import MobiliumClientNamespace
from mobilium_proto_messages.accessibility import Accessibility, AccessibilityById, AccessibilityByXpath
from mobilium_proto_messages.message_data_factory import MessageDataFactory
from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_proto_messages.proto.messages_pb2 import ElementNotExists
from socketio import Client


MessageResponse = TypeVar('MessageResponse')
FailureReason = TypeVar('FailureReason')


class MobiliumClient:

    def __init__(self):
        super().__init__()
        self.__client = Client()
        self.__namespace = '/client'
        self.__client_namespace = None
        self.__device_udid = None

    def connect(self, device_udid: str, address: str, port: int):
        print("Connect device_id %s" % device_udid)
        self.__device_udid = device_udid
        self.__client_namespace = MobiliumClientNamespace(self.__namespace, device_udid)
        self.__client.register_namespace(self.__client_namespace)
        self.__client.connect('tcp://{0}:{1}'.format(address, port))
        self.__wait_until_connected()

    def disconnect(self):
        print("Disconnect device_id %s" % self.__device_udid)
        self.__client.disconnect()
        self.__wait_until_disconnected()

    def prepare_driver(self):
        request = MessageDataFactory.prepare_driver_request()
        self.__send(request, MessageDeserializer.prepare_driver_response, timeout=300)
        print('after preparations')

    def start_driver(self):
        request = MessageDataFactory.start_driver_request(self.__device_udid)
        self.__send(request, MessageDeserializer.start_driver_response)

    def install_app(self, file_path: Optional[str] = None):
        if file_path is None:
            file_path = config.APP_FILE_PATH
        request = MessageDataFactory.install_app_request(self.__device_udid, file_path)
        self.__send(request, MessageDeserializer.install_app_response)

    def launch_app(self, bundle_id: Optional[str] = None):
        if bundle_id is None:
            bundle_id = config.APP_BUNDLE_ID
        request = MessageDataFactory.launch_app_request(bundle_id)
        self.__send(request, MessageDeserializer.launch_app_response)

    def uninstall_app(self, bundle_id: Optional[str] = None):
        if bundle_id is None:
            bundle_id = config.APP_BUNDLE_ID
        request = MessageDataFactory.uninstall_app_request(self.__device_udid, bundle_id)
        self.__send(request, MessageDeserializer.uninstall_app_response)

    def terminate_app(self):
        request = MessageDataFactory.terminate_app_request()
        self.__send(request, MessageDeserializer.terminate_app_response)

    def is_element_visible(self, accessibility: Accessibility, index: int = 0, timeout: float = 0) -> bool:
        request = MessageDataFactory.is_element_visible_request(accessibility, index=index, timeout=timeout)
        response = self.__send(request, MessageDeserializer.is_element_visible_response)
        return response.is_visible

    def is_element_invisible(self, accessibility: Accessibility, index: int = 0, timeout: float = 0) -> bool:
        request = MessageDataFactory.is_element_invisible_request(accessibility, index=index, timeout=timeout)
        response = self.__send(request, MessageDeserializer.is_element_invisible_response)
        return response.is_invisible

    def is_element_enabled(self, accessibility: Accessibility, index: int = 0) -> bool:
        request = MessageDataFactory.is_element_enabled_request(accessibility, index=index)
        response = self.__send(request, MessageDeserializer.is_element_enabled_response)
        return response.is_enabled

    def set_element_text(self, accessibility: Accessibility, text: str, index: int = 0, clears: bool = True):
        request = MessageDataFactory.set_element_text_request(accessibility, text=text, index=index, clears=clears)
        self.__send(request, MessageDeserializer.set_value_of_element_response)

    def set_slider_position(self, accessibility: Accessibility, position: float, index: int = 0):
        request = MessageDataFactory.set_position_request(accessibility, index=index, position=position)
        self.__send(request, MessageDeserializer.set_value_of_element_response)

    def get_element_value(self, accessibility: Accessibility, index: int = 0) -> str:
        request = MessageDataFactory.get_element_value_request(accessibility, index=index)
        response = self.__send(request, MessageDeserializer.get_value_of_element_response)
        return response.value

    def click_element(self, accessibility: Accessibility, index: int = 0):
        request = MessageDataFactory.click_element_request(accessibility, index=index)
        self.__send(request, MessageDeserializer.click_element_response)

    def get_elements_count(self, accessibility: Accessibility) -> int:
        request = MessageDataFactory.get_elements_count_request(accessibility)
        response = self.__send(request, MessageDeserializer.get_elements_count_response)
        return response.count

    def __send(self, request: bytes, deserialize: Callable[[bytes], Optional[MessageResponse]], timeout: int = 30)\
            -> MessageResponse:
        print("Send message, waiting for response {0}\n{1}".format(deserialize.__name__, request))
        self.__client.send(request, namespace=self.__namespace)
        response = self.__wait_for_first_matching_response(deserialize, timeout=timeout)
        print("Did receive response {0}\n{1}".format(deserialize.__name__, response))
        self.__handle_failure(response)
        return response

    def __handle_failure(self, response: Optional[MessageResponse]):
        if response is None or not hasattr(response, 'failure'):
            return
        failure = response.failure
        reason_attribute = failure.WhichOneof('reason')
        if reason_attribute is None:
            return
        reason = getattr(failure, reason_attribute)
        element_indicator = self.__element_indicator(response)
        self.__handle_failure_reason(reason, element_indicator=element_indicator)

    @staticmethod
    def __handle_failure_reason(reason: Optional[FailureReason], element_indicator: Optional[str]):
        if isinstance(reason, ElementNotExists):
            raise ElementNotFoundException(element_indicator)
        raise Exception("Not known failure reason from response")

    @staticmethod
    def __element_indicator(response: MessageResponse) -> Optional[str]:
        if not hasattr(response, 'element_indicator'):
            return None
        return getattr(response.element_indicator, response.element_indicator.WhichOneof('type'))

    def __is_connected(self) -> bool:
        return self.__client_namespace.is_connected

    def __is_disconnected(self) -> bool:
        return not self.__is_connected()

    def __wait_for_first_matching_response(self, deserialize: Callable[[bytes], Optional[MessageResponse]],
                                           timeout: int) -> MessageResponse:
        partial = named_partial(self.__client_namespace.read_first_matching_response, deserialize)
        response = wait_until_value(partial, timeout=timeout)
        self.__client_namespace.reset_responses_buffor()
        return response

    def __wait_until_connected(self):
        wait_until_true(self.__is_connected)

    def __wait_until_disconnected(self):
        wait_until_true(self.__is_disconnected)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--address", help="Mobilium Server IP Address", required=True)
    parser.add_argument("-p", "--port", help="Mobilium Server port. Default: 65432", default=65432)
    parser.add_argument("-u", "--udid", help="UDID of iOS device on which tests are run", required=True)
    arguments = parser.parse_args()

    mobilium_client = MobiliumClient()
    mobilium_client.connect(device_udid=arguments.udid, address=arguments.address, port=arguments.port)
    mobilium_client.start_driver()
    mobilium_client.install_app()
    mobilium_client.launch_app()

    mobilium_client.is_element_visible(AccessibilityById("login_button"))
    mobilium_client.is_element_invisible(AccessibilityById("unknown_button"))
    mobilium_client.is_element_enabled(AccessibilityById("login_button"))
    mobilium_client.click_element(AccessibilityByXpath("//XCUIElementTypeButton[contains(@label, 'tab_1')]"))

    time.sleep(1)

    mobilium_client.set_element_text(AccessibilityByXpath("//XCUIElementTypeTextField"
                                                          "[contains(@label, 'Your company (optional)')]"), "xpath\n")
    mobilium_client.set_element_text(AccessibilityById("email"), "homer123\n")
    mobilium_client.get_element_value(AccessibilityById("email"))
    mobilium_client.click_element(AccessibilityById("terms_checkbox"))

    mobilium_client.get_elements_count(AccessibilityByXpath("//XCUIElementTypeTextField[contains(@label, 'name')]"))

    mobilium_client.set_element_text(AccessibilityByXpath("//XCUIElementTypeTextField[contains(@label, 'name')]"),
                                     text="element at index 1", index=1)

    mobilium_client.terminate_app()
    mobilium_client.uninstall_app()
    mobilium_client.disconnect()


if __name__ == '__main__':
    main()
