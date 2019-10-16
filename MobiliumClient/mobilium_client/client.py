import argparse
from functools import partial
from typing import Optional, Callable, Any

from common.wait import wait_until
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
        print("Connect, device_id %s" % device_udid)
        self.__device_udid = device_udid
        self.__client_namespace = MobiliumClientNamespace(self.__namespace, device_udid)
        self.__client.register_namespace(self.__client_namespace)
        self.__client.connect('tcp://{0}:{1}'.format(address, port))
        self.__wait_for_connected()

    def disconnect(self):
        self.__client.disconnect()
        self.__wait_for_disconnected()

    def start_driver(self) -> Optional[StartDriverResponse]:
        print("Start driver")
        message = MessageDataFactory.start_driver_request(self.__device_udid)
        return self.send(message, MessageDeserializer.start_driver_response)

    def install_app(self) -> Optional[InstallAppResponse]:
        print("Install application")
        message = MessageDataFactory.install_app_request(self.__device_udid, config.APP_FILE_PATH)
        return self.send(message, MessageDeserializer.install_app_response)

    def launch_app(self) -> Optional[LaunchAppResponse]:
        print("Launch application")
        message = MessageDataFactory.launch_app_request(config.APP_BUNDLE_ID)
        return self.send(message, MessageDeserializer.launch_app_response)

    def uninstall_app(self) -> Optional[UninstallAppResponse]:
        print("Uninstall application")
        message = MessageDataFactory.uninstall_app_request(self.__device_udid, config.APP_BUNDLE_ID)
        return self.send(message, MessageDeserializer.uninstall_app_response)

    def terminate_app(self) -> Optional[TerminateAppResponse]:
        print("Terminate application")
        message = MessageDataFactory.terminate_app_request()
        return self.send(message, MessageDeserializer.terminate_app_response)

    def send(self, message: bytes, deserialize: Callable[[bytes], bool]) -> Optional[Any]:
        print('<<< {0}'.format(message))
        self.__client.send(message, namespace=self.__namespace)
        self.__wait_for_response(deserialize)
        response = self.__read_response(deserialize)
        self.__reset_response_data()
        return response

    def __is_connected(self) -> bool:
        return self.__client_namespace.is_connected

    def __is_not_connected(self) -> bool:
        return not self.__is_connected()

    def __read_response(self, deserialize: Callable[[bytes], bool]) -> Optional[Any]:
        return self.__client_namespace.read_response(deserialize)

    def __response_received(self, deserialize: Callable[[bytes], bool]) -> bool:
        return self.__read_response(deserialize) is not None

    def __reset_response_data(self):
        self.__client_namespace.reset_response_data()

    def __wait_for_response(self, deserialize: Callable[[bytes], bool]):
        response_received = partial(self.__response_received, deserialize)
        wait_until(response_received)

    def __wait_for_connected(self):
        wait_until(self.__is_connected)

    def __wait_for_disconnected(self):
        wait_until(self.__is_not_connected)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--address", help="Mobilium Server IP Address", required=True)
    parser.add_argument("-p", "--port", help="Mobilium Server port. Default: 65432", default=65432)
    parser.add_argument("-u", "--udid", help="UDID of iOS device on which tests are run", required=True)
    arguments = parser.parse_args()

    mobilium_client = MobiliumClient()
    mobilium_client.connect(device_udid=arguments.udid, address=arguments.address, port=arguments.port)
    print("main: did connect")
    mobilium_client.start_driver()
    print("main: did start driver")
    mobilium_client.install_app()
    print("main: did install app")
    mobilium_client.launch_app()
    print("main: did launch app")
    mobilium_client.send(MessageDataFactory.is_element_visible_request("login_button"),
                         MessageDeserializer.is_element_visible_response)
    print("main: did is element visible")
    mobilium_client.send(MessageDataFactory.set_element_text_request("password_field", "homer123\n"),
                         MessageDeserializer.set_value_of_element_response)
    print("main: did set text")
    response = mobilium_client.send(MessageDataFactory.get_element_value_request("password_field"),
                                    MessageDeserializer.get_value_of_element_response)
    print("main: did get element {}".format(response.value))
    mobilium_client.send(MessageDataFactory.click_element_request("login_field"),
                         MessageDeserializer.click_element_response)
    print("main: did click")
    mobilium_client.terminate_app()
    print("main: did terminate")
    mobilium_client.uninstall_app()
    print("main: did uninstall")
    mobilium_client.disconnect()
    print("main: did disconnect")


if __name__ == '__main__':
    main()
