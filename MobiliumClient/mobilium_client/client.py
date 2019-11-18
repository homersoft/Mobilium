# pylint: disable=E0611, E0401
import argparse
from typing import Optional, Callable, TypeVar
from common.named_partial import named_partial
from common.wait import wait_until_true, wait_until_value
from mobilium_client import config
from mobilium_client.client_namespace import MobiliumClientNamespace
from mobilium_proto_messages.accessibility import Accessibility, AccessibilityById, AccessibilityByXpath
from mobilium_proto_messages.message_data_factory import MessageDataFactory
from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_proto_messages.proto.messages_pb2 import StartDriverResponse, InstallAppResponse, LaunchAppResponse, \
    UninstallAppResponse, TerminateAppResponse, IsElementVisibleResponse, SetValueOfElementResponse, \
    GetValueOfElementResponse, ClickElementResponse, GetElementsCountResponse

from socketio import Client


MessageResponse = TypeVar('MessageResponse')


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

    def start_driver(self) -> Optional[StartDriverResponse]:
        request = MessageDataFactory.start_driver_request(self.__device_udid)
        return self.__send(request, MessageDeserializer.start_driver_response)

    def install_app(self) -> Optional[InstallAppResponse]:
        request = MessageDataFactory.install_app_request(self.__device_udid, config.APP_FILE_PATH)
        return self.__send(request, MessageDeserializer.install_app_response)

    def launch_app(self) -> Optional[LaunchAppResponse]:
        request = MessageDataFactory.launch_app_request(config.APP_BUNDLE_ID)
        return self.__send(request, MessageDeserializer.launch_app_response)

    def uninstall_app(self) -> Optional[UninstallAppResponse]:
        request = MessageDataFactory.uninstall_app_request(self.__device_udid, config.APP_BUNDLE_ID)
        return self.__send(request, MessageDeserializer.uninstall_app_response)

    def terminate_app(self) -> Optional[TerminateAppResponse]:
        request = MessageDataFactory.terminate_app_request()
        return self.__send(request, MessageDeserializer.terminate_app_response)

    def is_element_visible(self, accessibility: Accessibility, timeout: float = 0) -> Optional[IsElementVisibleResponse]:
        request = MessageDataFactory.is_element_visible_request(accessibility, timeout)
        return self.__send(request, MessageDeserializer.is_element_visible_response)

    def set_element_text(self, accessibility: Accessibility, text: str,
                         clears: bool = True) -> Optional[SetValueOfElementResponse]:
        request = MessageDataFactory.set_element_text_request(accessibility, text, clears)
        return self.__send(request, MessageDeserializer.set_value_of_element_response)

    def get_element_value(self, accessibility: Accessibility) -> Optional[GetValueOfElementResponse]:
        request = MessageDataFactory.get_element_value_request(accessibility)
        return self.__send(request, MessageDeserializer.get_value_of_element_response)

    def click_element(self, accessibility: Accessibility) -> Optional[ClickElementResponse]:
        request = MessageDataFactory.click_element_request(accessibility)
        return self.__send(request, MessageDeserializer.click_element_response)

    def get_elements_count(self, accessibility: Accessibility, timeout: float = 0) -> Optional[GetElementsCountResponse]:
        request = MessageDataFactory.get_elements_count_request(accessibility, timeout)
        return self.__send(request, MessageDeserializer.get_elements_count_response)

    def __send(self, request: bytes, deserialize: Callable[[bytes], Optional[MessageResponse]]) -> MessageResponse:
        print("Send message, waiting for response {0}\n{1}".format(deserialize.__name__, request))
        self.__client.send(request, namespace=self.__namespace)
        response = self.__wait_for_first_matching_response(deserialize)
        print("Did receive response {0}\n{1}".format(deserialize.__name__, response))
        return response

    def __is_connected(self) -> bool:
        return self.__client_namespace.is_connected

    def __is_disconnected(self) -> bool:
        return not self.__is_connected()

    def __wait_for_first_matching_response(self, deserialize: Callable[[bytes], Optional[MessageResponse]]) \
            -> MessageResponse:
        partial = named_partial(self.__client_namespace.read_first_matching_response, deserialize)
        response = wait_until_value(partial)
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
    mobilium_client.set_element_text(AccessibilityByXpath("//XCUIElementTypeTextField"
                                                          "[contains(@label, 'Email address')]"), "grzegorz.przybyla+test@silvair.com\n")
    mobilium_client.set_element_text(AccessibilityById("password_field"), "homer123\n")

    mobilium_client.get_elements_count(AccessibilityById("project_cell"), 5.0)
    mobilium_client.get_elements_count(AccessibilityByXpath("//XCUIElementTypeCell[contains(@value, 'Project_1')]"), 5.0)

    mobilium_client.terminate_app()
    mobilium_client.uninstall_app()
    mobilium_client.disconnect()


if __name__ == '__main__':
    main()
