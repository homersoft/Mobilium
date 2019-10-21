from typing import Callable, Optional, Any

from socketio import ClientNamespace
from mobilium_proto_messages.message_deserializer import MessageDeserializer


class MobiliumClientNamespace(ClientNamespace):

    def __init__(self, namespace: str, device_udid: str):
        super().__init__(namespace)
        self.__device_udid = device_udid
        self.is_connected = False
        self.__response_data_list = []

    def read_first_matching_response(self, deserialize: Callable[[bytes], Optional[Any]]) -> Optional[Any]:
        for data in self.__response_data_list:
            response = deserialize(data)
            if response is None:
                continue
            return response
        return None

    def reset_responses_buffor(self):
        self.__response_data_list = []

    def on_connect(self):
        print('Connected device_id %s' % self.__device_udid)
        self.is_connected = True

    def on_disconnect(self):
        print('Disconnected device_id %s' % self.__device_udid)
        self.is_connected = False

    def on_message(self, data):
        if data is not None:
            self.__response_data_list.append(data)

        response = MessageDeserializer.mobilium_message_response(data)
        if hasattr(response, 'failure') and response.HasField('failure'):
            print("Received message with error %s" % response.failure)
