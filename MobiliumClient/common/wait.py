import time
from typing import Callable


class TimeoutException(Exception):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


def wait_until(valid: Callable[[], bool], timeout: int = 30, timeout_message: str = None, interval: int = 1):
    end_time = time.time() + timeout
    while time.time() < end_time:
        if not valid():
            time.sleep(interval)
        else:
            return
    if timeout_message is None:
        timeout_message = '{} is False after {} seconds"'.format(valid.__name__, timeout)
    raise TimeoutException(timeout_message)
