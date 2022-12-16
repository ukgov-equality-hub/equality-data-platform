import mimetypes
from flask import Blueprint, url_for, Response
from edp_web.utils.config_helper import ConfigHelper
from edp_web.utils.decorators import EnterpriseTaskforcePasswordRequired, EnterpriseTaskforce2PasswordRequired
from edp_web.utils.redirect import local_redirect
from edp_web.utils.external_services.aws_s3_client import AwsS3Client

output = Blueprint('output', __name__)


@output.route('/output', methods=['GET'])
def output_index():
    return local_redirect(url_for('home.index'))


@output.route('/output/enterprise-taskforce', methods=['GET'])
def enterprise_taskforce_homepage_redirect():
    return local_redirect(url_for('output.enterprise_taskforce_homepage', page_path=''))


@output.route('/output/enterprise-taskforce/', defaults={'page_path': ''}, methods=['GET'])
@output.route('/output/enterprise-taskforce/<page_path>', methods=['GET'])
@EnterpriseTaskforcePasswordRequired
def enterprise_taskforce_homepage(page_path: str = ''):
    space_name = ConfigHelper.get_vcap_application().space_name
    s3_instance_name = f"{space_name}-filestorage-enterprise-taskforce"
    s3_client = AwsS3Client(instance_name=s3_instance_name)

    if page_path is None or page_path == '':
        page_path = 'index.html'
    if page_path.endswith('/'):
        page_path = page_path + 'index.html'

    file_bytes = s3_client.download_object(page_path)
    (mime_type, encoding) = mimetypes.guess_type(page_path)

    return Response(
        file_bytes,
        mimetype=mime_type
    )


@output.route('/output/enterprise-taskforce-no10-dashboard/', defaults={'page_path': ''}, methods=['GET'])
@output.route('/output/enterprise-taskforce-no10-dashboard/<path:page_path>', methods=['GET'])
@EnterpriseTaskforce2PasswordRequired
def enterprise_taskforce_2_homepage(page_path: str = ''):
    space_name = ConfigHelper.get_vcap_application().space_name
    s3_instance_name = f"{space_name}-filestorage-enterprise-taskforce-2"
    s3_client = AwsS3Client(instance_name=s3_instance_name)

    dir = '/output/enterprise-taskforce-no10-dashboard/'
    if page_path.startswith(dir):
        page_path = page_path[len(dir): ]

    if page_path is None or page_path == '':
        page_path = 'index.html'
    if page_path.endswith('/'):
        page_path = page_path + 'index.html'
    print(f'page_path: {page_path}', flush=True)

    file_bytes = s3_client.download_object(page_path)
    (mime_type, encoding) = mimetypes.guess_type(page_path)

    return Response(
        file_bytes,
        mimetype=mime_type
    )
