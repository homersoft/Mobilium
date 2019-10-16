import argparse

from mobilium_proto_messages.message_data_factory import MessageDataFactory
from mobilium_proto_messages.message_deserializer import MessageDeserializer

from socketio import Client, ClientNamespace

from mobilium_client import config


class MobiliumClientNamespace(ClientNamespace):

    def __init__(self, namespace: str, device_udid: str):
        super().__init__(namespace)
        self.device_udid = device_udid

    def on_connect(self):
        print('Connected')
        message = MessageDataFactory.start_driver_request(self.device_udid)
        self.send(message)

    def on_disconnect(self):
        print('Disconnected, device_id %s' % self.device_udid)

    def on_message(self, data):
        response = MessageDeserializer.mobilium_message_response(data)
        if hasattr(response, 'failure') and response.HasField('failure'):
            print("Received message with error %s" % response.failure)

        if MessageDeserializer.start_driver_response(data):
            message = MessageDataFactory.install_app_request(self.device_udid, config.APP_FILE_PATH)
            self.send(message)
        elif MessageDeserializer.install_app_response(data):
            message = MessageDataFactory.launch_app_request(config.APP_BUNDLE_ID)
            self.send(message)
        elif MessageDeserializer.launch_app_response(data):
            message = MessageDataFactory.is_element_visible_request("login_button")
            self.send(message)
        elif MessageDeserializer.is_element_visible_response(data):
            message = MessageDataFactory.set_element_text_request("password_field", "homer123\n")
            self.send(message)
        elif MessageDeserializer.set_value_of_element_response(data):
            message = MessageDataFactory.get_element_value_request("password_field")
            self.send(message)
        elif MessageDeserializer.get_value_of_element_response(data):
            message = MessageDataFactory.click_element_request("login_field")
            self.send(message)
        elif MessageDeserializer.click_element_response(data):
            message = MessageDataFactory.terminate_app_request()
            self.send(message)
        elif MessageDeserializer.terminate_app_response(data):
            message = MessageDataFactory.uninstall_app_request(self.device_udid, config.APP_BUNDLE_ID)
            self.send(message)
        elif MessageDeserializer.uninstall_app_response(data):
            self.disconnect()

    def send(self, message, room=None, skip_sid=None, namespace=None, callback=None):
        print('<<< {0}'.format(message))
        super(MobiliumClientNamespace, self).send(message, room=room, skip_sid=skip_sid, namespace=namespace, callback=callback)


def start_client(address: str, port: int, device_udid: str):
    client = Client()
    client.register_namespace(MobiliumClientNamespace('/client', device_udid))
    client.connect('tcp://{0}:{1}'.format(address, port))
    client.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--address", help="Mobilium Server IP Address", required=True)
    parser.add_argument("-p", "--port", help="Mobilium Server port. Default: 65432", default=65432)
    parser.add_argument("-u", "--udid", help="UDID of iOS device on which tests are run", required=True)
    arguments = parser.parse_args()
    start_client(arguments.address, arguments.port, arguments.udid)


if __name__ == '__main__':
    main()
