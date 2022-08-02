import os
import shutil
import time
from typing import List

from rap_web.utils.command_runner import CommandRunner
from rap_web.utils.git import Git
from rap_web.utils.pipelines import PipelineHelpers

working_directory='runner_workspace'
git = Git(working_directory=working_directory)
pipeline_helpers = PipelineHelpers(working_directory=working_directory)


class RapToRun:
    pipeline_slug: str
    run_number: int


def create_runs_for_raps_that_have_changed_since_they_were_last_run():
    git.fetch()
    branches = git.get_list_of_branches()
    for branch in branches:
        commit_sha = git.get_commit_sha_that_branch_points_to(branch)
        pipelines = pipeline_helpers.get_pipelines_for_branch(branch)
        for pipeline in pipelines:
            pipeline_run_for_current_commit = next(filter(lambda run: run.commit_sha == commit_sha, pipeline.runs), None)
            if pipeline_run_for_current_commit is None:
                print(f"Creating RAP for pipeline({pipeline.slug}) branch({branch}) commit({commit_sha})", flush=True)
                create_run_for_rap(pipeline.slug, branch, commit_sha)


def create_run_for_rap(pipeline_slug: str, branch: str, commit_sha: str):
    pipeline_dir = f"file_store/run_files/{pipeline_slug}/"
    if not os.path.exists(pipeline_dir):
        os.mkdir(pipeline_dir)

    run_dirs = os.scandir(f"file_store/run_files/{pipeline_slug}/")
    run_dirs = filter(lambda run_dir: run_dir.is_dir(), run_dirs)
    run_dir_names = map(lambda run_dir: run_dir.name, run_dirs)
    run_dir_names = filter(lambda run_dir_name: run_dir_name.startswith('run '), run_dir_names)
    run_numbers = map(lambda run_dir_name: int(run_dir_name[4:]), run_dir_names)

    next_run_number = max(run_numbers) + 1

    run_dir = f"{pipeline_dir}/run {next_run_number}"
    os.mkdir(run_dir)

    with open(f"{run_dir}/branch.txt", 'w') as file:
        file.write(branch)
    with open(f"{run_dir}/commit.txt", 'w') as file:
        file.write(commit_sha)


def find_raps_to_run() -> List[RapToRun]:
    raps_to_run: List[RapToRun] = []

    run_pipeline_dirs = os.scandir(f"file_store/run_files/")
    run_pipeline_dirs = filter(lambda run_dir: run_dir.is_dir(), run_pipeline_dirs)
    run_pipeline_dir_names = map(lambda run_dir: run_dir.name, run_pipeline_dirs)

    for pipeline_slug in run_pipeline_dir_names:
        run_dirs = os.scandir(f"file_store/run_files/{pipeline_slug}/")
        run_dirs = filter(lambda run_dir: run_dir.is_dir(), run_dirs)
        run_dir_names = map(lambda run_dir: run_dir.name, run_dirs)
        run_dir_names = filter(lambda run_dir_name: run_dir_name.startswith('run '), run_dir_names)
        run_numbers = map(lambda run_dir_name: int(run_dir_name[4:]), run_dir_names)

        for run_number in run_numbers:
            if not os.path.exists(f"file_store/run_files/{pipeline_slug}/run {run_number}/input_files"):
                # The input_files directory does not exist
                # So, this run hasn't been run yet
                # Add it to the list
                rap_to_run = RapToRun()
                rap_to_run.pipeline_slug = pipeline_slug
                rap_to_run.run_number = run_number
                raps_to_run.append(rap_to_run)

    return raps_to_run


def run_any_raps_that_need_running():
    raps_to_run = find_raps_to_run()
    print(f"Found ({len(raps_to_run)}) RAPs that need running", flush=True)

    for rap_to_run in raps_to_run:
        print(f"Running RAP pipeline_slug({rap_to_run.pipeline_slug}) run_number({rap_to_run.run_number})", flush=True)

        with open(f"file_store/run_files/{rap_to_run.pipeline_slug}/run {rap_to_run.run_number}/commit.txt", 'r') as file:
            commit_sha = file.read()
        with open(f"file_store/run_files/{rap_to_run.pipeline_slug}/run {rap_to_run.run_number}/branch.txt", 'r') as file:
            branch = file.read()
        git.git_checkout_commit(commit_sha)

        pipeline_steps = pipeline_helpers.get_pipeline_steps(rap_to_run.pipeline_slug)

        # Clean working directory
        pipeline_working_directory = f"{working_directory}/pipelines/{rap_to_run.pipeline_slug}/"
        if not os.path.exists(pipeline_working_directory):
            os.mkdir(pipeline_working_directory)

        data_dir = f"{pipeline_working_directory}/data"
        if os.path.exists(data_dir):
            files_to_delete = os.scandir(data_dir)
            for file_to_delete in files_to_delete:
                os.remove(file_to_delete.path)

        # Copy input_files from source to run_files
        input_files = pipeline_helpers.get_input_files(branch, rap_to_run.pipeline_slug)
        for input_file in input_files:
            source_dir = f"file_store/input_files/{rap_to_run.pipeline_slug}/{input_file.from_branch}"
            source_file = f"{source_dir}/{input_file.file_name}"
            dest_dir = f"file_store/run_files/{rap_to_run.pipeline_slug}/run {rap_to_run.run_number}/input_files"
            dest_file = f"{dest_dir}/{input_file.file_name}"
            dest2_dir = f"{working_directory}/pipelines/{rap_to_run.pipeline_slug}/data"
            dest2_file = f"{dest2_dir}/{input_file.file_name}"
            if not os.path.exists(source_dir):
                os.mkdir(source_dir)
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)
            if not os.path.exists(dest2_dir):
                os.mkdir(dest2_dir)
            shutil.copy(source_file, dest_file)
            shutil.copy(source_file, dest2_file)

        # Run each step
        command_runner = CommandRunner(working_directory=pipeline_working_directory)
        for pipeline_step in pipeline_steps:
            # Run the command
            console_output = command_runner.run_command(['Rscript', pipeline_step.file_full_name]).stdout

            # Save the console output
            console_output_dir = f"file_store/run_files/{rap_to_run.pipeline_slug}/run {rap_to_run.run_number}/step {pipeline_step.number}"
            console_output_file = f"{console_output_dir}/console_output.txt"
            if not os.path.exists(console_output_dir):
                os.mkdir(console_output_dir)
            with open(console_output_file, 'w') as file:
                file.write(console_output)

            # Copy the output files
            output_files = os.scandir(f"{working_directory}/pipelines/{rap_to_run.pipeline_slug}/data/")
            output_file_names = map(lambda run_dir: run_dir.name, output_files)
            for output_file_name in output_file_names:
                source_file = f"{working_directory}/pipelines/{rap_to_run.pipeline_slug}/data/{output_file_name}"
                dest_dir = f"file_store/run_files/{rap_to_run.pipeline_slug}/run {rap_to_run.run_number}/step {pipeline_step.number}/output_files"
                dest_file = f"{dest_dir}/{output_file_name}"
                if not os.path.exists(dest_dir):
                    os.mkdir(dest_dir)
                shutil.copy(source_file, dest_file)


while True:
    print("Creating any RAPs that need creating", flush=True)
    create_runs_for_raps_that_have_changed_since_they_were_last_run()

    print("Running any RAPs that need running", flush=True)
    run_any_raps_that_need_running()

    print("Sleeping", flush=True)
    time.sleep(10)
