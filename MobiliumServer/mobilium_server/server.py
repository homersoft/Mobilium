import argparse

from aiohttp import web
from socketio import AsyncServer

from mobilium_proto_messages.message_sender import MessageSender

from mobilium_server.message_processors.processor_factory import ProcessorFactory
from mobilium_server.message_broker import MessageBroker
from mobilium_server.message_handler import MessageHandler
from mobilium_server.remote_message_handler import RemoteMessageHandler


class Server(MessageHandler, MessageSender):

    def __init__(self, address: str, port: int):
        MessageHandler.__init__(self, 'server')
        self.address = address
        self.port = port
        self.app = web.Application()
        self.socket = AsyncServer(async_mode='aiohttp')
        self.socket.attach(self.app)
        self.broker = MessageBroker()
        self.broker.register_message_handler(self)
        self.processor = ProcessorFactory.make(self, address, port)

    async def process_message(self, data: bytes):
        await self.processor.process(data)

    def run(self):
        self.register_remote_message_handler('/client')
        self.register_remote_message_handler('/driver')
        web.run_app(self.app, host=self.address, port=self.port)

    def register_remote_message_handler(self, name: str):
        handler = RemoteMessageHandler(name)
        self.socket.register_namespace(handler)
        self.broker.register_message_handler(handler)

    async def send(self, data: bytes):
        await self.broker.process_message(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--address", help="Mobilium Server IP Address", required=True)
    parser.add_argument("-p", "--port", help="Mobilium Server port. Default: 65432", default=65432)
    arguments = parser.parse_args()
    Server(arguments.address, arguments.port).run()


if __name__ == '__main__':
    main()
