from mobilium_server.utils.shell_executor import ShellExecutor


class ShellExecutorPool:

    def __init__(self):
        self.executors = []

    def new_executor(self) -> ShellExecutor:
        executor = ShellExecutor()
        self.executors.append(executor)
        return executor
