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


def append_warning(html, warning):
    html = html.decode()
    if warning: warning = f'<span style="font-size: 14px; font-weight: normal; padding-left: 30px;">{warning}</span>'
    close = '<a href="javascript:;" style="position: absolute; right: 10px; font-weight: normal; color: #fff;" onclick="document.getElementById(\'warning\').style.display = \'none\'">Close</a>'

    html = html.replace('</body>', f'<div id="warning" style="position: fixed; bottom: 0; width: 100%; background: rgba(0, 0, 0, .6); color: #fff; text-align: center; font-family: \'GDS Transport\', Arial, sans-serif;"><p style="font-weight: bold; font-size: 18px;">OFFICIAL SENSITIVE do not forward or use externally without written permission{warning}{close}</p></div></body>')
    return str.encode(html)


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
        append_warning(file_bytes, 'Data extracted from Beauhurst December 2022'),
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
        append_warning(file_bytes, 'Data extracted from Beauhurst December 2022'),
        mimetype=mime_type
    )
