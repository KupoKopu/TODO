from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddToDoForm(FlaskForm):
    """Form for adding a to do item"""

    task = StringField('Task', validators=[
                       DataRequired(message="Task cannot be empty")])
    description = StringField('Description')
    submit = SubmitField('Submit')
