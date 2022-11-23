from functools import wraps
from flask import request, url_for, session, current_app
from edp_web.utils.redirect import local_redirect


def EnterpriseTaskforcePasswordRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'enterprise_taskforce_password' in session and session['enterprise_taskforce_password'] is not None:
            if session['enterprise_taskforce_password'] == current_app.config['ENTERPRISE_TASKFORCE_PASSWORD']:
                return f(*args, **kwargs)

        local_url = request.url[(len(request.host_url) - 1):]
        return local_redirect(url_for('login.login_get', return_to=local_url))

    return decorated_function


def EnterpriseTaskforce2PasswordRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'enterprise_taskforce_2_password' in session and session['enterprise_taskforce_2_password'] is not None:
            if session['enterprise_taskforce_2_password'] == current_app.config['ENTERPRISE_TASKFORCE_2_PASSWORD']:
                return f(*args, **kwargs)

        local_url = request.url[(len(request.host_url) - 1):]
        return local_redirect(url_for('login.login_get', return_to=local_url))

    return decorated_function
