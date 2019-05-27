from asyncio.subprocess import DEVNULL
from subprocess import Popen

from aiohttp import web
from socketio import AsyncServer

from mobilium_server.message_broker import MessageBroker
from mobilium_server.message_handler import MessageHandler
from mobilium_server.remote_message_handler import RemoteMessageHandler


class Server(MessageHandler):
    def __init__(self):
        MessageHandler.__init__(self, 'server')
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

    def start_driver(self):
        project = '../MobiliumDriver/MobiliumDriver.xcodeproj'
        scheme = 'MobiliumDriver'
        udid = '8b85dcfac17ce6251cda6c932ef0871a5e1603fa'
        command = 'xcodebuild -project {0} -scheme {1} -destination "platform=iOS,id={2}" test' \
            .format(project, scheme, udid)
        Popen(command, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, shell=True)

    def run(self):
        self.register_remote_message_handler('/client')
        self.register_remote_message_handler('/driver')
        web.run_app(self.app, host='192.168.52.93', port=65432)

    def register_remote_message_handler(self, name: str):
        handler = RemoteMessageHandler(name)
        self.socket.register_namespace(handler)
        self.broker.register_message_handler(handler)


if __name__ == '__main__':
    Server().run()
