import time
from typing import Callable, Any, Optional


class TimeoutException(Exception):

    def __init__(self, msg=None):
        self.msg = msg
        super().__init__()

    def __str__(self):
        return self.msg


def wait_until_true(action: Callable[[], bool], timeout: int = 30, interval: int = 1):
    def get_result():
        is_valid = action()
        if is_valid is None or is_valid is False:
            return None
        return True
    wait_until_not_none(get_result, timeout=timeout, interval=interval)


def wait_until_not_none(action: Callable[[], Any], timeout: int = 30, interval: int = 1) -> Optional[Any]:
    end_time = time.time() + timeout
    while time.time() < end_time:
        result = action()
        if result is None:
            time.sleep(interval)
        else:
            return result
    timeout_message = 'Timeout for {} after {} seconds"'.format(action.__name__, timeout)
    raise TimeoutException(timeout_message)
