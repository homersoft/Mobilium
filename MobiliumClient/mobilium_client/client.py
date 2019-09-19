import argparse
import asyncio

from mobilium_proto_messages.message_data_factory import MessageDataFactory
from mobilium_proto_messages.message_deserializer import MessageDeserializer

from socketio import AsyncClient, AsyncClientNamespace

from mobilium_client import config
from mobilium_client.message_validator import MessageValidator


class MobiliumClientNamespace(AsyncClientNamespace):

    def __init__(self, namespace: str, device_udid: str):
        super().__init__(namespace)
        self.device_udid = device_udid
        self.message_validator = MessageValidator()

    async def on_connect(self):
        print('Connected')
        message = MessageDataFactory.start_driver_request(self.device_udid)
        await self.send(message)

    async def on_disconnect(self):
        print('Disconnected')

    async def on_message(self, data):
        if MessageDeserializer.start_driver_response(data):
            message = MessageDataFactory.install_app_request(self.device_udid, config.APP_FILE_PATH)
            await self.send(message)
        elif MessageDeserializer.install_app_response(data):
            message = MessageDataFactory.launch_app_request(config.APP_BUNDLE_ID)
            await self.send(message)
        elif MessageDeserializer.launch_app_response(data):
            message = MessageDataFactory.is_element_visible_request("login_button")
            await self.send(message)
        elif MessageDeserializer.is_element_visible_response(data):
            self.message_validator.validate_is_element_visible_response(data=data, is_visible=True)
            message = MessageDataFactory.set_element_text_request("password_field", "homer123\n")
            await self.send(message)
        elif MessageDeserializer.set_value_of_element_response(data):
            self.message_validator.validate_set_value_of_element_response(data=data, success=True)
            message = MessageDataFactory.get_element_value_request("not_existing_element")
            await self.send(message)
        elif MessageDeserializer.get_value_of_element_response(data):
            self.message_validator.validate_element_not_exists(data, MessageDeserializer.get_value_of_element_response)
            message = MessageDataFactory.click_element_request("login_field")
            await self.send(message)
        elif MessageDeserializer.click_element_response(data):
            self.message_validator.validate_click_element_response(data=data, success=True)
            message = MessageDataFactory.terminate_app_request()
            await self.send(message)
        elif MessageDeserializer.terminate_app_response(data):
            message = MessageDataFactory.uninstall_app_request(self.device_udid, config.APP_BUNDLE_ID)
            await self.send(message)
        elif MessageDeserializer.uninstall_app_response(data):
            await self.disconnect()

    async def send(self, message, namespace=None, callback=None):
        print('<<< {0}'.format(message))
        await super(MobiliumClientNamespace, self).send(message, namespace=namespace, callback=callback)


async def start_client(address: str, port: int, device_udid: str):
    client = AsyncClient()
    client.register_namespace(MobiliumClientNamespace('/client', device_udid))
    await client.connect('tcp://{0}:{1}'.format(address, port))
    await client.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--address", help="Mobilium Server IP Address", required=True)
    parser.add_argument("-p", "--port", help="Mobilium Server port. Default: 65432", default=65432)
    parser.add_argument("-u", "--udid", help="UDID of iOS device on which tests are run", required=True)
    arguments = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_client(arguments.address, arguments.port, arguments.udid))


if __name__ == '__main__':
    main()
