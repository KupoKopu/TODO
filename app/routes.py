from flask import flash, redirect, render_template, url_for, request
from app import app, db
from app.forms import ToDoForm
from app.models import ToDo
import sqlalchemy as sa
import logging

logger = logging.getLogger('werkzeug')  # Get the underlying WSGI logger
handler = logging.FileHandler('app.log')  # Create a handler for the log file
logger.addHandler(handler)  # Add the handler to the werkzeug logger

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    allToDos = sa.select(ToDo)
    todos1 = db.session.scalars(allToDos).all()
    logger.info(todos1)
    
    return render_template('index.html', title='To Do', todos=todos1)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = ToDoForm()
    if form.validate_on_submit():
        todo = ToDo(task=form.task.data, description=form.description.data)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))


    return render_template('add.html', title='To Do', form=form)

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    try:
        db.session.delete(todo)
        db.session.commit()
        flash('Todo deleted successfully!', 'success')
    except:
        db.session.rollback()
        flash('Error deleting todo!', 'danger')
    return redirect(url_for('index'))
