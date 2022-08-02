from typing import List


class InputFile:
    file_name: str
    from_branch: str


class RunFile:
    file_name: str
    file_hash: str
    changed: bool


class PipelineRunStep:
    number: int
    name: str
    file_extension: str
    url_safe_filename: str
    output_files: List[RunFile]
    console_output: str

    def __init__(self):
        self.output_files = []

    @property
    def changed_files(self) -> List[RunFile]: return list(filter(lambda file: file.changed, self.output_files))
    @property
    def unchanged_files(self) -> List[RunFile]: return list(filter(lambda file: not file.changed, self.output_files))


class PipelineStep:
    number: int
    name: str
    file_extension: str
    file_full_name: str
    url_safe_filename: str


class PipelineRun:
    pipeline_slug: str
    pipeline_name: str
    number: int
    branch: str
    commit_sha: str
    commit_message: str
    input_files: List[RunFile]
    run_steps: List[PipelineRunStep]

    def __init__(self):
        self.input_files = []
        self.run_steps = []

    @property
    def any_run_steps(self) -> bool: return len(self.run_steps) > 0


class Pipeline:
    slug: str
    name: str
    steps: List[PipelineStep]
    use_files_from_own_branch: bool = False
    input_files: List[InputFile]
    runs: List[PipelineRun]

    def __init__(self):
        self.steps = []
        self.input_files = []
        self.runs = []