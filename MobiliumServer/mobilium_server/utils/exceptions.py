from typing import Optional


class MessageException(Exception):

    def __init__(self, message: Optional[str] = None):
        self.message = message
        super().__init__()

    def __str__(self):
        return self.message


class TimeoutException(MessageException):
    pass
