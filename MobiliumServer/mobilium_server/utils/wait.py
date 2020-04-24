from asyncio import sleep
from time import time
from typing import Callable, Optional

from mobilium_server.utils.exceptions import TimeoutException


async def wait_until_true(action: Callable[[], bool], timeout: int = 30, interval: int = 1,
                          timeout_message: Optional[str] = None):
    end_time = time() + timeout
    while time() < end_time:
        if action():
            return
        await sleep(interval)
    if timeout_message is None:
        timeout_message = "Timeout for {} after {} seconds".format(action.__name__, timeout)
    raise TimeoutException(timeout_message)
