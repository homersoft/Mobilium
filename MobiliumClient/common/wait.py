import time
from typing import Callable, Optional, TypeVar

from common.exceptions import TimeoutException

WaitValue = TypeVar('WaitValue')


def wait_until_true(action: Callable[[], bool], timeout: int = 30, interval: int = 1):
    def get_result() -> Optional[bool]:
        return True if action() else None
    wait_until_value(get_result, timeout=timeout, interval=interval)


def wait_until_value(action: Callable[[], Optional[WaitValue]], timeout: int = 30, interval: int = 1) -> WaitValue:
    end_time = time.time() + timeout
    while time.time() < end_time:
        result = action()
        if result is None:
            time.sleep(interval)
        else:
            return result
    timeout_message = 'Timeout for {} after {} seconds"'.format(action.__name__, timeout)
    raise TimeoutException(timeout_message)
