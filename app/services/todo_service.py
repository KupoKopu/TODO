from flask import flash

from app import db
from app.exceptions.exceptions import TodoNotFoundException
from app.models import ToDo
from app.services.logger_service import setup_logger

logger = setup_logger()


def add_todo(task, description):
    try:
        todo = ToDo(task=task, description=description)
        db.session.add(todo)
        db.session.commit()
        logger.info(f'Inserted to_do: {todo}')

    except Exception as e:
        db.session.rollback()
        logger.error(f'Error inserting to_do: {e}')
        flash('An error occurred while processing your request. Check logs for more information.',
              'error')


def get_all_todos():
    try:
        result = ToDo.query.all()
        logger.info(f'Getting all from to_do: {result}')
        return result

    except Exception as e:
        logger.error(f'Error getting todos: {e}')
        flash('An error occurred while processing your request. Check logs for more information.',
              'error')
        return []


def delete_todo(todo_id):
    try:
        todo = ToDo.query.get(todo_id)

        if (todo is None):
            raise TodoNotFoundException(todo_id)

        db.session.delete(todo)
        db.session.commit()
        logger.info(f'Deleted to_do: {todo}')

    except TodoNotFoundException as e:
        logger.error(e.__str__())
        flash('Cannot delete a non-existing todo.', 'error')
        db.session.rollback()


def edit_todo(todo_id, task, description):
    try:
        todo = ToDo.query.get(todo_id)

        if (todo is None):
            raise TodoNotFoundException(todo_id)
        if not task:
            raise ValueError('Task cannot be empty.')

        todo.task = task
        todo.description = description
        db.session.commit()
        logger.info(f'Updated to_do: {todo}')

    except TodoNotFoundException as e:
        logger.error(e.__str__())
        flash('Cannot edit a non-existing todo.', 'error')
        db.session.rollback()
    except ValueError as e:
        logger.error(f'Error updating to_do: {e}')
        flash(e.__str__(), 'error')
        db.session.rollback()


def get_todo_by_id(todo_id):
    try:
        todo = ToDo.query.get(todo_id)

        if (todo is None):
            raise TodoNotFoundException(todo_id)

        logger.info(f'Getting to_do: {todo}')
        return todo

    except TodoNotFoundException as e:
        logger.error(e.__str__())
        flash('Cannot get a non-existing todo.', 'error')
        return None
