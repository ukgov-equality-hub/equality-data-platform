from flask import Blueprint, render_template, abort, current_app, session, request
from edp_web.login.forms import PasswordForm
from edp_web.utils.redirect import local_redirect

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET'])
def login_get():
    form = PasswordForm()

    return render_template(
        'login/login.html',
        form=form
    )


@login.route('/login', methods=['POST'])
def login_post():
    if not request.args['return_to'].startswith('/'):
        abort(404)

    form = PasswordForm()

    if form.validate():
        if form.password.data == current_app.config['ENTERPRISE_TASKFORCE_PASSWORD'] and request.args['return_to'] == '/output/enterprise-taskforce/':
            session['enterprise_taskforce_password'] = form.password.data
            return local_redirect(request.args['return_to'])

        elif form.password.data == current_app.config['ENTERPRISE_TASKFORCE_2_PASSWORD'] and request.args['return_to'] == '/output/enterprise-taskforce-no10-dashboard/':
            session['enterprise_taskforce_2_password'] = form.password.data
            return local_redirect(request.args['return_to'])

        else:
            form.password.errors.append('Enter the correct password')

    return render_template(
        'login/login.html',
        form=form
    )
