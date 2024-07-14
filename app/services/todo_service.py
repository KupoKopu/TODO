from app import db
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


def get_all_todos():
    try:
        result = ToDo.query.all()
        logger.info(f'Getting all from to_do: {result}')
        return result

    except Exception as e:
        logger.error(f'Error getting todos: {e}')
        return []
