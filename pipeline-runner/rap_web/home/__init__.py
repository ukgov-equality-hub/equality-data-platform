import time

from flask import Blueprint, render_template, url_for, send_file

from rap_web.home.forms import NewBranchForm, NewPipelineForm, NewStepForm
from rap_web.utils.git import Git
from rap_web.utils.pipelines import PipelineHelpers
from rap_web.utils.redirect import local_redirect

home = Blueprint('home', __name__)

working_directory='raps'
git = Git(working_directory=working_directory)
pipeline_helpers = PipelineHelpers(working_directory=working_directory)


@home.route('/', methods=['GET'])
def index():
    return render_template('home/index.html')


@home.route('/health-check', methods=['GET'])
def health_check():
    return render_template('home/health-check.html')


@home.route('/data-store', methods=['GET'])
def data_store():
    return render_template('home/data-store.html')


@home.route('/data-store/file-group-1/2021', methods=['GET'])
def data_store_file_group_1_2021():
    return render_template('home/data-store-file-group-1-2021.html')


@home.route('/data-store/file-group-1/2021/add-a-file', methods=['GET'])
def data_store_add_a_file():
    return render_template('home/data-store-add-a-file.html')


@home.route('/data-store/file-group-1/2021/use-in-pipeline', methods=['GET'])
def use_in_pipeline():
    return render_template('home/use-in-pipeline.html')


@home.route('/data-store/publish-files', methods=['GET'])
def publish_files():
    return render_template('home/publish-files.html')


@home.route('/branches', methods=['GET'])
def branches():
    list_of_branches = git.get_list_of_branches()
    return render_template(
        'home/branches.html',
        branches=list_of_branches
    )


@home.route('/new-branch', methods=['GET', 'POST'])
def new_branch():
    form = NewBranchForm()

    list_of_branches = git.get_list_of_branches()
    branches_options = [{'Value': '', 'Option': ''}]
    for branch in list_of_branches:
        branches_options.append({'Value': branch, 'Option': branch})

    if form.validate_on_submit():
        git.create_new_branch(form.branch_name.data, form.create_from_branch.data)
        return local_redirect(url_for('home.branches'))

    return render_template(
        'home/new-branch.html',
        form=form,
        branches_options=branches_options
    )


@home.route('/branches/<branch>/pipelines', methods=['GET'])
def pipelines_for_branch(branch: str):
    pipelines = pipeline_helpers.get_list_of_pipeline_names_for_branch(branch)

    return render_template(
        'home/pipelines.html',
        branch=branch,
        pipelines=pipelines
    )


@home.route('/branches/<branch>/new-pipeline', methods=['GET', 'POST'])
def new_pipeline(branch: str):
    form = NewPipelineForm()

    if form.validate_on_submit():
        pipeline_helpers.create_new_pipeline(branch, form.pipeline_name.data)
        return local_redirect(url_for('home.pipelines_for_branch', branch=branch))

    return render_template(
        'home/new-pipeline.html',
        form=form,
        branch=branch,
    )


def timer(tic: float, step_finished: str):
    toc = time.perf_counter()
    print(f"Step ({step_finished}) took {toc - tic:0.4f}", flush=True)
    return toc

@home.route('/branches/<branch>/pipelines/<pipeline_slug>', methods=['GET'])
def pipeline_info(branch: str, pipeline_slug: str):
    tic = time.perf_counter()
    tic = timer(tic, 'Fetch')

    pipeline = pipeline_helpers.get_pipeline_data(branch,
                                                  pipeline_slug,
                                                  runs_to_include=5,
                                                  include_run_steps=False,
                                                  include_pipeline_name=False)
    tic = timer(tic, 'Get pipelines data')

    return render_template(
        'home/pipeline.html',
        branch=branch,
        pipeline=pipeline
    )


@home.route('/branches/<branch>/pipelines/<pipeline_slug>/new-step', methods=['GET', 'POST'])
def new_step(branch: str, pipeline_slug: str):
    form = NewStepForm()
    pipeline = pipeline_helpers.get_pipeline_data(branch,
                                                  pipeline_slug,
                                                  include_steps=False,
                                                  include_input_files=False,
                                                  include_runs=False)

    if form.validate_on_submit():
        pipeline_helpers.create_new_pipeline_step(branch, pipeline_slug, form.step_name.data)
        return local_redirect(url_for('home.pipeline_info', branch=branch, pipeline_slug=pipeline_slug))

    return render_template(
        'home/new-step.html',
        form=form,
        branch=branch,
        pipeline=pipeline
    )


@home.route('/pipeline-runs/<pipeline_slug>/run-<run_number>', methods=['GET'])
def pipeline_run(pipeline_slug: str, run_number: int):
    pipeline_run = pipeline_helpers.get_pipeline_run_data(pipeline_slug, run_number)

    return render_template(
        'home/pipeline-run.html',
        pipeline_run=pipeline_run
    )


@home.route('/pipeline-runs/<pipeline_slug>/run-<run_number>/input-files/<file_name>', methods=['GET'])
def download_pipeline_input_file(pipeline_slug: str, run_number: int, file_name: str):
    file_path = rf"..\file_store\run_files\{pipeline_slug}\run {run_number}\input_files\{file_name}"
    return send_file(file_path, attachment_filename=file_name)


@home.route('/pipeline-runs/<pipeline_slug>/run-<run_number>/step-<step_number>/output-files/<file_name>', methods=['GET'])
def download_pipeline_run_file(pipeline_slug: str, run_number: int, step_number: int, file_name: str):
    file_path = rf"..\file_store\run_files\{pipeline_slug}\run {run_number}\step {step_number}\output_files\{file_name}"
    return send_file(file_path, attachment_filename=file_name)
