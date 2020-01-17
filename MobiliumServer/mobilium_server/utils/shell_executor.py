from typing import Optional
from subprocess import DEVNULL, STDOUT
from asyncio.subprocess import Process
import asyncio


class ShellExecutor:

    def __init__(self):
        self.process: Optional[Process] = None

    async def execute(self, command: str, track_output: bool = False, waits_for_termination: bool = True):
        print('Run: %s', command)
        if self.process is not None and self.process.returncode is None:
            print("Killing already running process")
            self.process.kill()
        self.process = await asyncio.create_subprocess_shell(
            command, stdin=DEVNULL, stdout=asyncio.subprocess.PIPE, stderr=STDOUT)

        if track_output:
            print("Tracking process output")
            await asyncio.ensure_future(self.__output_reader())

        if waits_for_termination:
            print("Waiting until process finishes")
            await self.process.wait()

    async def __output_reader(self):
        while True:
            line = await self.process.stdout.readline()
            if line == b'':
                break
            print(line.decode("latin").rstrip())
