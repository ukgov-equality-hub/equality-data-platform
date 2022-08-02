from typing import List

from rap_web.utils.command_runner import CommandRunner


class Git:
    working_directory: str
    command_runner: CommandRunner

    def __init__(self, working_directory: str):
        self.working_directory = working_directory
        self.command_runner = CommandRunner(working_directory=working_directory)

    def get_list_of_branches(self):
        git_branch_command_result = self.run_command(['git', 'branch', '-r'])

        branch_list = git_branch_command_result.stdout.split('\n')
        branch_list = map(lambda branch: branch.strip(), branch_list)
        branch_list = filter(lambda branch: branch.startswith('origin/'), branch_list)
        branch_list = map(lambda branch: branch[7:], branch_list)
        branch_list = filter(lambda branch: not branch.__contains__('->'), branch_list)

        return branch_list

    def checkout_branch(self, branch: str, create_local_branch: bool = False):
        git_branch_command_result = self.run_command(['git', 'branch', '--show-current']).stdout.strip()
        if not git_branch_command_result == branch:
            self.run_command(['git', 'checkout', '--force', f"origin/{branch}"])
            if create_local_branch:
                self.run_command(['git', 'branch', '-D', branch])
                self.run_command(['git', 'branch', branch])
                self.run_command(['git', 'switch', branch])

    def add(self, file_to_add: str):
        self.run_command(['git', 'add', file_to_add])

    def commit(self, commit_message: str):
        self.run_command(['git', 'commit', '-m', commit_message])

    def push(self, branch: str):
        self.run_command(['git', 'push', 'origin', branch])

    def git_get_commit_message(self, commit_sha: str):
        return self.run_command(['git', 'log', '--format=%B', '-n', '1', commit_sha]).stdout

    def git_checkout_commit(self, commit_sha: str):
        self.run_command(['git', 'checkout', '--force', commit_sha])

    def does_commit_exist(self, commit_sha: str):
        command_output = self.run_command(['git', 'cat-file', '-t', commit_sha]).stdout.strip()
        return command_output == 'commit'

    def git_calculate_file_hash(self, file_path: str):
        self.run_command(['git', 'hash-object', f"--path={file_path}"])

    def fetch(self):
        self.run_command(['git', 'fetch'])

    def get_commit_sha_that_branch_points_to(self, branch: str):
        return self.run_command(['git', 'rev-list', '-n', '1', f"origin/{branch}"]).stdout.strip()

    def create_new_branch(self, branch: str, create_from_branch: str):
        # run_command(['git', 'fetch'])
        self.run_command(['git', 'checkout', '--force', f"origin/{create_from_branch}"])
        self.run_command(['git', 'branch', branch])
        self.run_command(['git', 'push', 'origin', branch])

    def run_command(self, command: List[str]):
        return self.command_runner.run_command(command)
