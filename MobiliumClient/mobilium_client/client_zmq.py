import asyncio
import logging
import json
import signal
import zmq
import zmq.asyncio


async def pop(socket):
    *envelope, payload = await socket.recv_multipart()
    message = json.loads(payload.decode('utf-8'))
    return tuple(envelope) + (message, )


async def push(socket, *parts):
    *envelope, message = parts
    payload = b'HelloClient'
    await socket.send_multipart(tuple(envelope) + (payload, ))


class Client:
    def __init__(self, host='192.168.52.49', port=65432):
        self.host = host
        self.port = port

    async def start(self, context):
        logger = logging.getLogger('client')

        socket = context.socket(zmq.REQ)
        socket.connect('tcp://{0}:{1}'.format(self.host, self.port))

        await socket.send(b'HelloClient')
        response = await socket.recv()
        logger.info(response)

        await socket.send(b'RunDriver')
        response = await socket.recv()
        logger.info(response)


def main():
    logging.basicConfig(level=logging.INFO)
    context = zmq.asyncio.Context.instance()
    loop = asyncio.get_event_loop()
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    loop.run_until_complete(Client().start(context))


if __name__ == '__main__':
    main()
