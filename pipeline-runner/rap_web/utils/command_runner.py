import subprocess
from typing import List


class CommandRunner:
    working_directory: str

    def __init__(self, working_directory: str):
        self.working_directory = working_directory

    def run_command(self, command: List[str]):
        return subprocess.run(command, cwd=self.working_directory, capture_output=True, encoding='UTF-8')
