from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired


class ToDoForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    description = StringField('Description')
    is_complete = BooleanField('Is Complete')
    submit = SubmitField('Submit')
