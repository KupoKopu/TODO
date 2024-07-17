from flask import flash

from app import db
from app.exceptions.exceptions import TodoNotFoundException
from app.models import ToDo
from app.services.logger_service import setup_logger

logger = setup_logger()


def add_todo(task, description):
    """
    Adds a new ToDo item to the database.

    Args:
        task (str): The task name.
        description (str): The description of the task.

    Returns:
        None
    """
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
    """
    Retrieves all todos from the database.

    Returns:
        A list of all todos in the database.
    """
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
    """
    Deletes a todo item from the database.

    Args:
        todo_id (int): The ID of the todo item to be deleted.

    Returns:
        None

    Effects:
        The todo item with the given ID is deleted from the database.

    Raises:
        TodoNotFoundException: If the todo item with the given ID does not exist.
    """
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
    """
    Edit a todo item with the given todo_id.

    Args:
        todo_id (int): The ID of the todo item to be edited.
        task (str): The updated task for the todo item.
        description (str): The updated description for the todo item.

    Returns:
        None

    Effects:
        The task and description of the todo item with the given todo_id are updated

    Raises:
        TodoNotFoundException: If the todo item with the given todo_id does not exist.
        ValueError: If the task is empty.
    """
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
    """
    Retrieve a todo item by its ID.

    Args:
        todo_id (int): The ID of the todo item to retrieve.

    Returns:
        ToDo: The todo item with the specified ID, if found.
        None: If the todo item with the specified ID does not exist.

    Raises:
        TodoNotFoundException: If the todo item with the specified ID does not exist.
    """
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
