import os
from datetime import timedelta
from flask import Flask, g
from edp_web.config import Config, DevConfig, TestConfig
from edp_web.utils.build_info import get_build_info
from edp_web.utils.compiled_css_js_filenames import get_app_css_filename, get_app_js_filename
from edp_web.utils.http_basic_authentication import HttpBasicAuthentication
from edp_web.utils.maintenance_mode import Maintenance
from edp_web.utils.custom_error_handlers import CustomErrorHandlers


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if os.environ['FLASK_ENV'] == 'production':
        config_object = Config
    elif os.environ['FLASK_ENV'] == 'development':
        config_object = DevConfig
    else:
        config_object = TestConfig

    app.config.from_object(config_object)

    if os.environ['FLASK_ENV'] != 'development':
        CustomErrorHandlers(app)

    # Show "Service unavailable" page if the config setting it set
    if app.config['MAINTENANCE_MODE'] == 'ON':
        Maintenance(app)
        return app

    # Require HTTP Basic Authentication if both the username and password are set
    if app.config['BASIC_AUTH_USERNAME'] and app.config['BASIC_AUTH_PASSWORD']:
        HttpBasicAuthentication(app)

    # Load build info from JSON file
    build_info = get_build_info()

    # Load compiled app.css and app.js filenames
    app_css_filename = get_app_css_filename()
    app_js_filename = get_app_js_filename()


    # Update session timeout time
    @app.before_request
    def make_before_request():
        app.permanent_session_lifetime = timedelta(hours=24)
        g.build_info = build_info
        if os.environ['FLASK_ENV'] == 'development':
            g.app_css_filename = get_app_css_filename()
            g.app_js_filename = get_app_js_filename()
        else:
            g.app_css_filename = app_css_filename
            g.app_js_filename = app_js_filename


    @app.after_request
    def add_header(response):
        response.headers['X-Frame-Options'] = 'deny'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # response.headers['Content-Security-Policy'] = "default-src 'self'; " \
        #                                                 "script-src 'self' 'unsafe-inline'; " \
        #                                                 "script-src-elem 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com; " \
        #                                                 "script-src-attr 'self' 'unsafe-inline'; " \
        #                                                 "style-src 'self' 'unsafe-inline'; " \
        #                                                 "img-src 'self'; " \
        #                                                 "font-src 'self'; " \
        #                                                 "connect-src 'self' https://www.google-analytics.com; " \
        #                                                 "form-action 'self';"

        return response

    # Home
    from edp_web.home import home
    app.register_blueprint(home)

    # Login pages
    from edp_web.login import login
    app.register_blueprint(login)

    # Output (i.e. reports or publications)
    from edp_web.output import output
    app.register_blueprint(output)

    # Allow additional "/assets" URL for static assets
    from edp_web.assets import assets
    app.register_blueprint(assets)

    return app
