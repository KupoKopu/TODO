from app import db
from app.models import ToDo


def get_all_todos():
    return ToDo.query.all()


def add_todo(task, description):
    try:
        todo = ToDo(task=task, description=description)
        db.session.add(todo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
