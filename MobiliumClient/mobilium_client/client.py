import argparse
import asyncio

from mobilium_proto_messages.MessageDataFactory import MessageDataFactory
from mobilium_proto_messages.MessageDeserializer import MessageDeserializer
from socketio import AsyncClient, AsyncClientNamespace


class MobiliumClientNamespace(AsyncClientNamespace):
    async def on_connect(self):
        print('Connected')
        message = MessageDataFactory.start_driver_request()
        await self.send(message)

    async def on_disconnect(self):
        print('Disconnected')

    async def on_message(self, data):
        if MessageDeserializer.start_driver_response(data):
            message = MessageDataFactory.install_app_request()
            await self.send(message)
        elif MessageDeserializer.install_app_response(data):
            message = MessageDataFactory.execute_test_request()
            await self.send(message)
        elif MessageDeserializer.execute_test_response(data):
            message = MessageDataFactory.uninstall_app_request()
            await self.send(message)
        elif MessageDeserializer.uninstall_app_response(data):
            await self.disconnect()

    async def send(self, message, namespace=None, callback=None):
        print('<<< {0}'.format(message))
        await super(MobiliumClientNamespace, self).send(message, namespace=namespace, callback=callback)


async def start_client(address: str, port: int):
    client = AsyncClient()
    client.register_namespace(MobiliumClientNamespace('/client'))
    await client.connect('tcp://{0}:{1}'.format(address, port))
    await client.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--address", help="Mobilium Server IP Address", required=True)
    parser.add_argument("-p", "--port", help="Mobilium Server port. Default: 65432", default=65432)
    arguments = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_client(arguments.address, arguments.port))


if __name__ == '__main__':
    main()
