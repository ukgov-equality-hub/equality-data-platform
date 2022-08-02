from flask import Blueprint, send_from_directory

assets = Blueprint('assets', __name__)


@assets.route('/assets/<path:path>', methods=['GET'])
def asset(path):
    return send_from_directory('static/assets', path)
