from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ToDoForm(FlaskForm):
    """Form for adding and editing a to do item"""

    task = StringField('Task', validators=[
                       DataRequired(message="Task cannot be empty")])
    description = StringField('Description')
    submit = SubmitField('Submit')
