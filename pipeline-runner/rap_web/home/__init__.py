from flask import Blueprint, render_template

home = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
def index():
    return render_template('home/index.html')


@home.route('/health-check', methods=['GET'])
def health_check():
    return render_template('home/health-check.html')
