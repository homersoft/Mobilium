from subprocess import Popen, DEVNULL


class ShellExecutor:

    @staticmethod
    def execute(command: str, waits_for_termination: bool = True):
        print('Run: "{}"...'.format(command))
        process = Popen(command, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, shell=True)
        if waits_for_termination:
            process.wait()
            print('...process finished')
