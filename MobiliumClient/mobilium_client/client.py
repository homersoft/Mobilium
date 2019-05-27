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
            await self.send('ExecuteTest')
        if message == 'TestExecuted':
            await self.disconnect()

    async def send(self, message):
        print('<<< {0}'.format(message))
        await super(AsyncClientNamespace, self).send(message)


async def start_client():
    client = AsyncClient()
    client.register_namespace(MobiliumClientNamespace('/client'))
    await client.connect('tcp://192.168.52.93:65432')
    await client.wait()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_client())
