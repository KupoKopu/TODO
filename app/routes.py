from flask import redirect, render_template, url_for

from app import app
from app.forms import AddToDoForm
from app.services import todo_service


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    todos = todo_service.get_all_todos()

    return render_template('index.html', title='To Do', todos=todos)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddToDoForm()
    if form.validate_on_submit():
        if todo_service.add_todo(form.task.data, form.description.data):
            return redirect(url_for('index'))

    return render_template('add.html', title='To Do', form=form)
