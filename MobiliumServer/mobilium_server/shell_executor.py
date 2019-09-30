from subprocess import Popen, DEVNULL, PIPE
import threading


class ShellExecutor:

    @staticmethod
    def output_reader(process):
        lines_iterator = iter(process.stdout.readline, b'')
        for line in lines_iterator:
            nline = line.rstrip()
            print(nline.decode("latin"), end="\r\n", flush=True)  # yield line

    @staticmethod
    def execute(command: str, track_output: bool = False, waits_for_termination: bool = True):
        print('Run: "{}"...'.format(command))
        process = Popen(command, stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL, shell=True)

        if track_output:
            thread = threading.Thread(target=ShellExecutor.output_reader, args=(process,))
            thread.start()

        if waits_for_termination:
            process.wait()
            print('...process finished')
