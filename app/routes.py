from flask import Blueprint, redirect, render_template, url_for

from app.forms import ToDoForm
from app.services import todo_service

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    todos = todo_service.get_all_todos()

    return render_template('index.html', title='To Do', todos=todos)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = ToDoForm()
    if form.validate_on_submit():
        todo_service.add_todo(form.task.data, form.description.data)
        return redirect(url_for('main.index'))

    return render_template('add.html', title='To Do', form=form)


@bp.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo_service.delete_todo(todo_id)
    return redirect(url_for('main.index'))


@bp.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    todo = todo_service.get_todo_by_id(todo_id)
    form = ToDoForm()
    if form.validate_on_submit():
        todo_service.edit_todo(
            todo_id, form.task.data, form.description.data)
        return redirect(url_for('main.index'))

    form.task.data = todo.task
    form.description.data = todo.description
    form.validate()

    return render_template('edit.html', title='To Do', form=form)
