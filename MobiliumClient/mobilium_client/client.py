import argparse
from typing import Optional, Callable, Any

from common.named_partial import named_partial
from common.wait import wait_until_true, wait_until_not_none
from mobilium_client import config
from mobilium_client.client_namespace import MobiliumClientNamespace
from mobilium_proto_messages.message_data_factory import MessageDataFactory, StartDriverResponse, InstallAppResponse, \
    UninstallAppResponse, TerminateAppResponse, LaunchAppResponse
from mobilium_proto_messages.message_deserializer import MessageDeserializer

from socketio import Client


class MobiliumClient:

    def __init__(self, ):
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
        self.__wait_for_connected()

    def disconnect(self):
        print("Disconnect device_id %s" % self.__device_udid)
        self.__client.disconnect()
        self.__wait_for_disconnected()

    def start_driver(self) -> Optional[StartDriverResponse]:
        message = MessageDataFactory.start_driver_request(self.__device_udid)
        return self.send(message, MessageDeserializer.start_driver_response)

    def install_app(self) -> Optional[InstallAppResponse]:
        message = MessageDataFactory.install_app_request(self.__device_udid, config.APP_FILE_PATH)
        return self.send(message, MessageDeserializer.install_app_response)

    def launch_app(self) -> Optional[LaunchAppResponse]:
        message = MessageDataFactory.launch_app_request(config.APP_BUNDLE_ID)
        return self.send(message, MessageDeserializer.launch_app_response)

    def uninstall_app(self) -> Optional[UninstallAppResponse]:
        message = MessageDataFactory.uninstall_app_request(self.__device_udid, config.APP_BUNDLE_ID)
        return self.send(message, MessageDeserializer.uninstall_app_response)

    def terminate_app(self) -> Optional[TerminateAppResponse]:
        message = MessageDataFactory.terminate_app_request()
        return self.send(message, MessageDeserializer.terminate_app_response)

    def send(self, message: bytes, deserialize: Callable[[bytes], Optional[Any]]) -> Optional[Any]:
        print("Send message [{0}]\n{1}".format(deserialize.__name__, message))
        self.__client.send(message, namespace=self.__namespace)
        response = self.__wait_for_first_matching_response(deserialize)
        print("Did receive response [{0}]\n{1}".format(deserialize.__name__, response))
        return response

    def __is_connected(self) -> bool:
        return self.__client_namespace.is_connected

    def __is_not_connected(self) -> bool:
        return not self.__is_connected()

    def __wait_for_first_matching_response(self, deserialize: Callable[[bytes], bool]) -> Optional[Any]:
        partial = named_partial(self.__client_namespace.read_first_matching_response, deserialize)
        response = wait_until_not_none(partial)
        self.__client_namespace.reset_responses_buffor()
        return response

    def __wait_for_connected(self):
        wait_until_true(self.__is_connected)

    def __wait_for_disconnected(self):
        wait_until_true(self.__is_not_connected)


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
    mobilium_client.send(MessageDataFactory.is_element_visible_request("login_button"),
                         MessageDeserializer.is_element_visible_response)
    mobilium_client.send(MessageDataFactory.set_element_text_request("password_field", "homer123\n"),
                         MessageDeserializer.set_value_of_element_response)
    mobilium_client.send(MessageDataFactory.get_element_value_request("password_field"),
                         MessageDeserializer.get_value_of_element_response)
    mobilium_client.send(MessageDataFactory.click_element_request("login_field"),
                         MessageDeserializer.click_element_response)
    mobilium_client.terminate_app()
    mobilium_client.uninstall_app()
    mobilium_client.disconnect()


if __name__ == '__main__':
    main()
