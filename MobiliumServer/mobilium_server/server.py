import argparse
from asyncio.subprocess import DEVNULL
from subprocess import Popen

from aiohttp import web
from socketio import AsyncServer

from mobilium_server.message_broker import MessageBroker
from mobilium_server.message_handler import MessageHandler
from mobilium_server.remote_message_handler import RemoteMessageHandler


class Server(MessageHandler):
    udid = '3adbc878f0b32c44a296c2fc62f46fe50c548355'
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

    async def process_message(self, message: str):
        if message == 'Run':
            self.run()
        if message == 'StartDriver':
            self.start_driver()
        if message == 'InstallApp':
            await self.install_app()
        if message == 'UninstallApp':
            await self.uninstall_app()

    async def install_app(self):
        command = 'ideviceinstaller -u {0} -i {1}'.format(self.udid, self.ipa_path)
        self.open(command)
        await self.send_message('AppInstalled')

    async def uninstall_app(self):
        command = 'ideviceinstaller -U {}'.format(self.bundle_id)
        self.open(command)
        await self.send_message('AppUninstalled')

    def start_driver(self):
        project = '../MobiliumDriver/MobiliumDriver.xcodeproj'
        scheme = 'MobiliumDriver'
        command = 'xcodebuild -project {0} -scheme {1} -destination "platform=iOS,id={2}" HOST={3} PORT={4} test' \
            .format(project, scheme, self.udid, self.address, self.port)
        self.open(command, waits=False)

    def run(self):
        self.register_remote_message_handler('/client')
        self.register_remote_message_handler('/driver')
        web.run_app(self.app, host=self.address, port=self.port)

    def register_remote_message_handler(self, name: str):
        handler = RemoteMessageHandler(name)
        self.socket.register_namespace(handler)
        self.broker.register_message_handler(handler)

    def open(self, command: str, waits: bool = True):
        print('Run: "{}"...'.format(command))
        process = Popen(command, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, shell=True)
        if waits:
            process.wait()
            print('...process finished'.format(command))

    async def send_message(self, message: str):
        await self.broker.process_message(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--address", help="Mobilium Server IP Address", required=True)
    parser.add_argument("-p", "--port", help="Mobilium Server port. Default: 65432", default=65432)
    arguments = parser.parse_args()
    Server(arguments.address, arguments.port).run()


if __name__ == '__main__':
    main()
