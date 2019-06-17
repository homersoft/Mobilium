import argparse
import asyncio

from socketio import AsyncClient, AsyncClientNamespace


class MobiliumClientNamespace(AsyncClientNamespace):
    async def on_connect(self):
        print('Connected')
        await self.send('StartDriver')

    async def on_disconnect(self):
        print('Disconnected')

    async def on_message(self, message):
        print('>>> {0}'.format(message))
        if message == 'DriverStarted':
            await self.send('InstallApp')
        if message == 'AppInstalled':
            await self.send('ExecuteTest')
        if message == 'TestExecuted':
            await self.send('UninstallApp')
        if message == 'AppUninstalled':
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
