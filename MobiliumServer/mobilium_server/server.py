import argparse
from asyncio.subprocess import DEVNULL
from subprocess import Popen

from aiohttp import web
from mobilium_proto_messages.message_data_factory import MessageDataFactory
from mobilium_proto_messages.message_deserializer import MessageDeserializer
from socketio import AsyncServer

from mobilium_server.message_broker import MessageBroker
from mobilium_server.message_handler import MessageHandler
from mobilium_server.remote_message_handler import RemoteMessageHandler


class Server(MessageHandler):
    bundle_id = 'com.silvair.commissioning.test.dev'
    ipa_path = './app.ipa'

    def __init__(self, address: str, port: int):
        MessageHandler.__init__(self, 'server')
        self.address = address
        self.port = port
        self.app = web.Application()
        self.socket = AsyncServer(async_mode='aiohttp')
        self.socket.attach(self.app)
        self.broker = MessageBroker()
        self.broker.register_message_handler(self)

    async def process_message(self, data: bytes):
        if await self.handle_start_driver(data):
            pass
        elif await self.handle_install_app(data):
            pass
        elif await self.handle_uninstall_app(data):
            pass

    async def handle_start_driver(self, data: bytes) -> bool:
        message = MessageDeserializer.start_driver_request(data)
        if message is not None:
            self.start_driver(message.udid)
            return True
        return False

    async def handle_install_app(self, data: bytes) -> bool:
        message = MessageDeserializer.install_app_request(data)
        if message is not None:
            await self.install_app(message.udid)
            return True
        return False

    async def handle_uninstall_app(self, data: bytes) -> bool:
        message = MessageDeserializer.uninstall_app_request(data)
        if message is not None:
            await self.uninstall_app(message.udid)
            return True
        return False

    async def install_app(self, udid: str):
        command = 'ideviceinstaller -u {0} -i {1}'.format(udid, self.ipa_path)
        self.open(command)
        message = MessageDataFactory.install_app_response()
        await self.send_message(message)

    async def uninstall_app(self, udid: str):
        command = 'ideviceinstaller -u {0} -U {1}'.format(udid, self.bundle_id)
        self.open(command)
        message = MessageDataFactory.uninstall_app_response()
        await self.send_message(message)

    def start_driver(self, udid: str):
        project = '../MobiliumDriver/MobiliumDriver.xcodeproj'
        scheme = 'MobiliumDriver'
        command = 'xcodebuild -project {0} -scheme {1} -destination "platform=iOS,id={2}" HOST={3} PORT={4} test' \
            .format(project, scheme, udid, self.address, self.port)
        self.open(command, waits_for_termination=False)

    def run(self):
        self.register_remote_message_handler('/client')
        self.register_remote_message_handler('/driver')
        web.run_app(self.app, host=self.address, port=self.port)

    def register_remote_message_handler(self, name: str):
        handler = RemoteMessageHandler(name)
        self.socket.register_namespace(handler)
        self.broker.register_message_handler(handler)

    def open(self, command: str, waits_for_termination: bool = True):
        print('Run: "{}"...'.format(command))
        process = Popen(command, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, shell=True)
        if waits_for_termination:
            process.wait()
            print('...process finished')

    async def send_message(self, message: bytes):
        await self.broker.process_message(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--address", help="Mobilium Server IP Address", required=True)
    parser.add_argument("-p", "--port", help="Mobilium Server port. Default: 65432", default=65432)
    arguments = parser.parse_args()
    Server(arguments.address, arguments.port).run()


if __name__ == '__main__':
    main()
