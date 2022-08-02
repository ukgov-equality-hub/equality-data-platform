import os
import re


# Load compiled app.css filename
def get_app_css_filename():
    for file in os.listdir('./rap_web/static/assets/'):
        if re.compile('^app-[0-9a-f]+\.css$').match(file):
            return file
    return 'foo'

# Load compiled app.js filename
def get_app_js_filename():
    for file in os.listdir('./rap_web/static/assets/'):
        if re.compile('^app-[0-9a-f]+\.js$').match(file):
            return file
    return 'foo'
