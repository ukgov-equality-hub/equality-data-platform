import os
import re
import time
from typing import List
from urllib.parse import quote_plus

from rap_web.data_model.data_model import Pipeline, PipelineStep, InputFile, PipelineRun, RunFile, PipelineRunStep
from rap_web.utils.git import Git
from rap_web.utils.slugify import slugify, filename_safe


def timer(tic: float, step_finished: str):
    toc = time.perf_counter()
    # print(f"Step ({step_finished}) took {toc - tic:0.4f}", flush=True)
    return toc


class PipelineHelpers:
    working_directory: str
    git: Git

    def __init__(self, working_directory):
        self.working_directory = working_directory
        self.git = Git(working_directory=working_directory)

    def get_list_of_pipeline_names_for_branch(self, branch: str) -> List[Pipeline]:
        return self.get_pipelines_for_branch(branch, include_steps=False, include_input_files=False, include_runs=False)

    def get_pipelines_for_branch(self, branch: str, include_steps=True, include_input_files=True, include_runs=True) -> List[Pipeline]:
        self.git.checkout_branch(branch)

        pipeline_folder_names = os.scandir('raps/pipelines')
        pipeline_folder_names = filter(lambda pipeline: pipeline.is_dir(), pipeline_folder_names)
        pipeline_folder_names = map(lambda pipeline: pipeline.name, pipeline_folder_names)

        pipelines: List[Pipeline] = []
        for pipeline_folder_name in pipeline_folder_names:
            pipeline = self.get_pipeline_data(branch,
                                              pipeline_folder_name,
                                              include_steps=include_steps,
                                              include_input_files=include_input_files,
                                              include_runs=include_runs)
            if pipeline is not None:
                pipelines.append(pipeline)

        return pipelines

    def get_pipeline_data(self, branch: str,
                          pipeline_slug: str,
                          include_steps: bool = True,
                          include_input_files: bool = True,
                          include_runs: bool = True,
                          runs_to_include: int = None,
                          include_run_steps: bool = True,
                          include_pipeline_name: bool = True
                          ) -> Pipeline | None:
        tic = time.perf_counter()

        self.git.checkout_branch(branch)
        tic = timer(tic, 'Git checkout')

        if os.path.exists(f"raps/pipelines/{pipeline_slug}/NAME.txt"):
            tic = timer(tic, 'Check NAME.txt')
            pipeline = Pipeline()

            # Slug and name
            pipeline.slug = pipeline_slug
            with open(f"raps/pipelines/{pipeline_slug}/NAME.txt", 'r') as file:
                pipeline.name = file.read()
            tic = timer(tic, 'Read NAME.txt')

            # Pipeline Steps
            if include_steps:
                pipeline.steps = self.get_pipeline_steps(pipeline_slug)
            tic = timer(tic, 'Pipeline steps')

            # Input files
            if include_input_files:
                pipeline.input_files = self.get_input_files(branch, pipeline_slug)
                if len(pipeline.input_files) > 0:
                    pipeline.use_files_from_own_branch = pipeline.input_files[0].from_branch != 'main'
            tic = timer(tic, 'Input files')

            # Runs
            if include_runs:
                run_dirs = os.scandir(f"file_store/run_files/{pipeline_slug}/")
                run_dirs = filter(lambda run_dir: run_dir.is_dir(), run_dirs)
                run_dir_names = map(lambda run_dir: run_dir.name, run_dirs)
                run_dir_names = filter(lambda run_dir_name: run_dir_name.startswith('run '), run_dir_names)
                run_dir_numbers = list(map(lambda run_dir_name: int(run_dir_name[4:]), run_dir_names))
                run_dir_numbers.sort(key=lambda run_dir_number: run_dir_number, reverse=True)
                if runs_to_include is not None:
                    actual_runs_to_include = min(runs_to_include, len(run_dir_numbers))
                    run_dir_numbers = run_dir_numbers[:actual_runs_to_include]
                run_dir_numbers.sort(key=lambda run_dir_number: run_dir_number)

                for run_dir_number in run_dir_numbers:
                    pipeline_run = self.get_pipeline_run_data(pipeline_slug,
                                                              run_number=run_dir_number,
                                                              include_run_steps=include_run_steps,
                                                              include_pipeline_name=include_pipeline_name)
                    pipeline.runs.append(pipeline_run)
                pipeline.runs.sort(key=lambda pipeline_run: pipeline_run.number, reverse=True)
            tic = timer(tic, 'Runs')

            return pipeline

        else:
            return None

    def get_pipeline_steps(self, pipeline_slug: str) -> List[PipelineStep]:
        pipeline_steps: List[PipelineStep] = []

        pipeline_files = os.scandir(f"{self.working_directory}/pipelines/{pipeline_slug}/")
        pipeline_file_names = map(lambda pipeline_file: pipeline_file.name, pipeline_files)
        for pipeline_file_name in pipeline_file_names:
            regex_result = re.search(r'(\d*) - (.*)\.(.*)', pipeline_file_name)
            if regex_result is not None:
                step = PipelineStep()
                step.file_full_name = pipeline_file_name
                step.number = int(regex_result.group(1))
                step.name = regex_result.group(2)
                step.file_extension = regex_result.group(3)
                step.url_safe_filename = quote_plus(pipeline_file_name).replace('+', '%20')
                pipeline_steps.append(step)

        return pipeline_steps

    def get_input_files(self, branch: str, pipeline_slug: str) -> List[InputFile]:
        input_file_objs: List[InputFile] = []

        if os.path.exists(f"file_store/input_files/{pipeline_slug}/{branch}"):
            input_files = os.scandir(f"file_store/input_files/{pipeline_slug}/{branch}")
            for input_file in input_files:
                input_file_obj = InputFile()
                input_file_obj.file_name = input_file.name
                input_file_obj.from_branch = branch
                input_file_objs.append(input_file_obj)
        elif os.path.exists(f"file_store/input_files/{pipeline_slug}/main"):
            input_files = os.scandir(f"file_store/input_files/{pipeline_slug}/main")
            for input_file in input_files:
                input_file_obj = InputFile()
                input_file_obj.file_name = input_file.name
                input_file_obj.from_branch = 'main'
                input_file_objs.append(input_file_obj)

        return input_file_objs

    def get_pipeline_run_data(self, pipeline_slug: str,
                              run_number: int,
                              include_run_steps: bool = True,
                              include_pipeline_name: bool = True
                              ) -> PipelineRun:
        pipeline_run = PipelineRun()
        pipeline_run.pipeline_slug = pipeline_slug
        pipeline_run.number = run_number

        with open(f"file_store/run_files/{pipeline_slug}/run {pipeline_run.number}/branch.txt", 'r') as file:
            pipeline_run.branch = file.read()

        with open(f"file_store/run_files/{pipeline_slug}/run {pipeline_run.number}/commit.txt", 'r') as file:
            pipeline_run.commit_sha = file.read()

        pipeline_run.commit_message = self.git.git_get_commit_message(pipeline_run.commit_sha)

        # Load run input files
        run_input_files_dir = f"file_store/run_files/{pipeline_slug}/run {pipeline_run.number}/input_files/"
        if os.path.exists(run_input_files_dir):
            run_input_files = os.scandir(run_input_files_dir)
            run_input_file_names = map(lambda file: file.name, run_input_files)
            for run_input_file_name in run_input_file_names:
                run_input_file = RunFile()
                run_input_file.file_name = run_input_file_name
                input_file_path = f"file_store/run_files/{pipeline_slug}/run {pipeline_run.number}/input_files/{run_input_file_name}"
                run_input_file.file_hash = self.git.git_calculate_file_hash(input_file_path)
                pipeline_run.input_files.append(run_input_file)

        if include_pipeline_name or include_run_steps:
            if not self.git.does_commit_exist(pipeline_run.commit_sha):
                self.git.fetch()
            self.git.git_checkout_commit(pipeline_run.commit_sha)

        # Get pipeline name
        if include_pipeline_name:
            with open(f"raps/pipelines/{pipeline_slug}/NAME.txt", 'r') as file:
                pipeline_run.pipeline_name = file.read()

        # Load run steps
        if include_run_steps:
            pipeline_files = os.scandir(f"raps/pipelines/{pipeline_slug}/")
            pipeline_file_names = map(lambda pipeline_file: pipeline_file.name, pipeline_files)
            for pipeline_file_name in pipeline_file_names:
                regex_result = re.search(r'(\d*) - (.*)\.(.*)', pipeline_file_name)
                if regex_result is not None:
                    step = PipelineRunStep()
                    step.number = int(regex_result.group(1))
                    step.name = regex_result.group(2)
                    step.file_extension = regex_result.group(3)
                    step.url_safe_filename = quote_plus(pipeline_file_name).replace('+', '%20')
                    console_output_file_path = f"file_store/run_files/{pipeline_slug}/run {pipeline_run.number}/step {step.number}/console_output.txt"
                    if os.path.exists(console_output_file_path):
                        with open(console_output_file_path, 'r') as file:
                            step.console_output = file.read()

                    run_step_output_files_dir = f"file_store/run_files/{pipeline_slug}/run {pipeline_run.number}/step {step.number}/output_files"
                    if os.path.exists(run_step_output_files_dir):
                        run_step_output_files = os.scandir(run_step_output_files_dir)
                        run_step_output_file_names = map(lambda file: file.name, run_step_output_files)
                        for file_name in run_step_output_file_names:
                            run_file = RunFile()
                            run_file.file_name = file_name
                            run_file_path = f"file_store/run_files/{pipeline_slug}/run {pipeline_run.number}/step {step.number}/output_files/{file_name}"
                            run_file.file_hash = self.git.git_calculate_file_hash(run_file_path)
                            run_file.changed = self.calculate_changed(run_file, step.number, pipeline_run.run_steps, pipeline_run.input_files)
                            step.output_files.append(run_file)

                    pipeline_run.run_steps.append(step)



        return pipeline_run

    def calculate_changed(self, run_file: RunFile, step_number: int, run_steps: List[PipelineRunStep], input_files: List[RunFile]):
        if step_number == 1:
            files_from_previous_step = input_files
        else:
            previous_step = next(filter(lambda step: step.number == step_number - 1, run_steps), None)
            files_from_previous_step = previous_step.output_files

        file_from_previous_step = next(filter(lambda file: file.file_name == run_file.file_name, files_from_previous_step), None)
        if file_from_previous_step is None:
            return True
        else:
            return file_from_previous_step.file_hash != run_file.file_hash

    def create_new_pipeline(self, branch: str, pipeline_name: str):
        self.git.checkout_branch(branch, create_local_branch=True)

        slugified_pipeline_name = slugify(pipeline_name)
        if not os.path.exists(f"raps/pipelines/{slugified_pipeline_name}"):
            os.mkdir(f"raps/pipelines/{slugified_pipeline_name}")
        with open(f"raps/pipelines/{slugified_pipeline_name}/NAME.txt", 'w') as file:
            file.write(pipeline_name)

        name_file = f"pipelines/{slugified_pipeline_name}/NAME.txt"
        self.git.add(name_file)
        commit_message = f"Created pipeline '{pipeline_name}'"
        self.git.commit(commit_message)
        self.git.push(branch)

    def create_new_pipeline_step(self, branch: str, pipeline_slug: str, step_name: str):
        self.git.checkout_branch(branch, create_local_branch=True)

        current_steps = self.get_pipeline_steps(pipeline_slug)
        current_step_numbers = map(lambda step: step.number, current_steps)
        next_step_number = max(current_step_numbers) + 1

        filename_safe_step_name = filename_safe(step_name)
        git_relative_file_path = f"pipelines/{pipeline_slug}/{next_step_number} - {filename_safe_step_name}.R"
        new_step_file_path = f"raps/{git_relative_file_path}"
        with open(new_step_file_path, 'w') as file:
            file.write(f"\nprint('Running pipeline {pipeline_slug} step {next_step_number}')\n")

        self.git.add(git_relative_file_path)
        commit_message = f"Added step #{next_step_number} to pipeline {pipeline_slug}"
        self.git.commit(commit_message)
        self.git.push(branch)
