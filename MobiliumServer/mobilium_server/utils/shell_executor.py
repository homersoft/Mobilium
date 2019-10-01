from subprocess import Popen, DEVNULL, PIPE
import threading


class ShellExecutor:

    def __init__(self):
        self.process = None
        self.thread = None

    def output_reader(self):
        lines_iterator = iter(self.process.stdout.readline, b'')
        for line in lines_iterator:
            nline = line.rstrip()
            print(nline.decode("latin"), end="\r\n", flush=True)

    def execute(self, command: str, track_output: bool = False, waits_for_termination: bool = True):
        print('Run: %s', command)
        if self.process is not None and self.process.poll() is None:
            print("Killing already running process")
            self.process.kill()
        self.process = Popen(command, stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL, shell=True)

        if track_output:
            self.thread = threading.Thread(target=self.output_reader)
            self.thread.setDaemon(True)
            self.thread.start()

        if waits_for_termination:
            self.process.wait()
            print('...process finished')
