from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class NewBranchForm(FlaskForm):
    branch_name = StringField(
        validators=[
            DataRequired(message='Enter a branch name')
        ]
    )

    create_from_branch = StringField(
        validators=[
            DataRequired(message='Enter a branch name')
        ]
    )


class NewPipelineForm(FlaskForm):
    pipeline_name = StringField(
        validators=[
            DataRequired(message='Enter a name for this pipeline')
        ]
    )


class NewStepForm(FlaskForm):
    step_name = StringField(
        validators=[
            DataRequired(message='Enter a name for this step')
        ]
    )
