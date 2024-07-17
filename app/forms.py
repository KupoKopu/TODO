from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ToDoForm(FlaskForm):
    """
    Represents a form for creating or editing a ToDo task.
    """
    task = StringField('Task', validators=[
                       DataRequired(message="Task cannot be empty")])
    description = StringField('Description')
    submit = SubmitField('Submit')
