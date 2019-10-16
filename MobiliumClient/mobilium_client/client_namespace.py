from typing import Callable, Optional, Any

from socketio import ClientNamespace
from mobilium_proto_messages.message_deserializer import MessageDeserializer


class MobiliumClientNamespace(ClientNamespace):

    def __init__(self, namespace: str, device_udid: str):
        super().__init__(namespace)
        self.__device_udid = device_udid
        self.is_connected = False
        self.__response_data_list = []

    def read_response(self, deserialize: Callable[[bytes], bool]) -> Optional[Any]:
        for data in self.__response_data_list:
            response = deserialize(data)
            if response is None:
                continue
            else:
                return response
        return None

    def reset_response_data(self):
        self.__response_data_list = []

    def on_connect(self):
        print('Connected, device_id %s' % self.__device_udid)
        self.is_connected = True

    def on_disconnect(self):
        print('Disconnected, device_id %s' % self.__device_udid)
        self.is_connected = False

    def on_message(self, data):
        if data is not None:
            self.__response_data_list.append(data)

        response = MessageDeserializer.mobilium_message_response(data)
        if hasattr(response, 'failure') and response.HasField('failure'):
            print("Received message with error %s" % response.failure)
        else:
            print("Received message without errors")

        if MessageDeserializer.start_driver_response(data):
            print("received start driver")
        elif MessageDeserializer.install_app_response(data):
            print("received install app")
        elif MessageDeserializer.launch_app_response(data):
            print("received launch app")
        elif MessageDeserializer.is_element_visible_response(data):
            print("received is element visible")
        elif MessageDeserializer.set_value_of_element_response(data):
            print("received set value")
        elif MessageDeserializer.get_value_of_element_response(data):
            print("received get value")
        elif MessageDeserializer.click_element_response(data):
            print("received click element")
        elif MessageDeserializer.terminate_app_response(data):
            print("received terminate app")
        elif MessageDeserializer.uninstall_app_response(data):
            print("received uninstall app")
