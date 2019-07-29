import argparse
import asyncio

from google.protobuf.message import Message
from mobilium_proto_messages.MessageDataFactory import MessageDataFactory
from socketio import AsyncClient, AsyncClientNamespace

import mobilium_client.proto.messages_pb2 as proto


class MobiliumClientNamespace(AsyncClientNamespace):
    async def on_connect(self):
        print('Connected')
        message = MessageDataFactory.start_driver_request()
        await self.send(message)

    async def on_disconnect(self):
        print('Disconnected')

    async def on_message(self, data):
        if isinstance(data, bytes):
            mobilium_message: Message = proto.MobiliumMessage().FromString(data)
            message = getattr(mobilium_message, mobilium_message.WhichOneof('message'))
            if isinstance(message, proto.StartDriverResponse):
                await self.send('InstallApp')
        else:
            if data == 'AppInstalled':
                message = MessageDataFactory.execute_test_request()
                await self.send(message)
            if data == 'TestExecuted':
                await self.send('UninstallApp')
            if data == 'AppUninstalled':
                await self.disconnect()

    async def send(self, message, namespace=None, callback=None):
        if isinstance(message, Message):
            data = message.SerializeToString()
            print('<<< {0}'.format(message))
            await super(MobiliumClientNamespace, self).send(data, namespace=namespace, callback=callback)
        else:
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
