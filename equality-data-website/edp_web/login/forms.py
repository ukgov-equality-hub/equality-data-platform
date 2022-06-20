from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class PasswordForm(FlaskForm):
    password = StringField(
        validators=[
            DataRequired(message='Enter a password')
        ]
    )
