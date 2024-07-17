import unittest
from unittest.mock import patch

import sqlalchemy as sa
from flask import url_for

from app import create_app, db
from app.models import ToDo
from app.services import todo_service
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SERVER_NAME = 'localhost.localdomain'
    WTF_CSRF_ENABLED = False


class ToDoModelCase(unittest.TestCase):
    """Unit tests for the ToDo model"""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_todo(self):
        todos = ToDo.query.all()
        self.assertEqual(todos, [], "no todos at start")
        todo = ToDo(task="test", description="test description")
        db.session.add(todo)
        db.session.commit()
        todos = db.session.scalars(sa.select(ToDo)).all()
        self.assertEqual(todos.__len__(), 1, "todo has inserted")

        db.session.rollback()

    def test_add_todo_fails_with_missing_task(self):
        todo = ToDo(description="Missing task")
        db.session.add(todo)
        with self.assertRaises(sa.exc.IntegrityError):
            db.session.commit()

            db.session.rollback()

    def test_add_todo_with_missing_description(self):
        todo = ToDo(task="Missing Description")
        db.session.add(todo)
        db.session.commit()

        added_todo = ToDo.query.filter_by(
            task="Missing Description").first()
        self.assertIsNotNone(added_todo)

        db.session.rollback()

    def test_add_todo_fails_with_task_exceeding_max_length(self):
        long_task = "x" * 33

        with self.assertRaises(ValueError):
            todo = ToDo(task=long_task,
                        description="Normal description")
            db.session.add(todo)
            db.session.commit()

            db.session.rollback()

    def test_add_todo_fails_with_description_exceeding_max_length(self):
        long_description = "x" * 300
        with self.assertRaises(ValueError):
            todo = ToDo(task="Long Description Task",
                        description=long_description)
            db.session.add(todo)
            db.session.commit()

            db.session.rollback()


class FlaskRoutesTestCase(unittest.TestCase):
    """Integration tests using flask routes"""

    def setUp(self):
        app = create_app(TestConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_open_index_page(self):
        response = self.app.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'To Do', response.data)

    def test_open_add_page(self):
        response = self.app.get(url_for('main.add'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add To Do', response.data)

    def test_add_route_post(self):
        response = self.app.post(url_for('main.add'), data={
            'task': "Test Task",
            'description': "Test Description"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task', response.data)

        todo = ToDo.query.first()
        self.assertIsNotNone(todo)
        self.assertEqual(todo.task, "Test Task")

    def test_edit_post(self):
        todo = ToDo(task="Test Task", description="Test Description")
        db.session.add(todo)
        db.session.commit()

        response = self.app.post(url_for('main.edit', todo_id=todo.id), data={
            'task': "New Task",
            'description': "New Description"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Task', response.data)

        updated_todo = ToDo.query.get(todo.id)
        self.assertEqual(updated_todo.task, "New Task")


class TestToDoService(unittest.TestCase):
    """Unit Tests for the ToDo service"""

    def setUp(self):
        app = create_app(TestConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.services.todo_service.logger')
    @patch('app.db.session.add')
    def test_add_todo_success(self, mock_db_add, mock_logger):
        todo_service.add_todo('Test Task', 'Test Description')
        mock_db_add.assert_called()
        mock_logger.error.assert_not_called()

    @patch('app.services.todo_service.logger')
    @patch('app.models.ToDo.query')
    def test_get_all_todos_success(self, mock_query, mock_logger):
        mock_query.all.return_value = [
            ToDo(task='Test Task', description='Test Description')]
        result = todo_service.get_all_todos()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].task, 'Test Task')
        self.assertEqual(result[0].description, 'Test Description')
        mock_logger.error.assert_not_called()

    @patch('app.services.todo_service.flash')
    @patch('app.services.todo_service.logger')
    @patch('app.db.session.add')
    def test_add_todo_exception(self, mock_db_add, mock_logger, mock_flash):
        mock_db_add.side_effect = Exception('Test exception')
        todo_service.add_todo('Test Task', 'Test Description')
        mock_flash.assert_called_with(
            'An error occurred while processing your request. Check logs for more information.', 'error')
        mock_logger.error.assert_called()

    @patch('app.services.todo_service.flash')
    @patch('app.services.todo_service.logger')
    @patch('app.models.ToDo.query')
    def test_get_all_todos_exception(self, mock_query, mock_logger, mock_flash):
        mock_query.all.side_effect = Exception('Test exception')
        result = todo_service.get_all_todos()
        self.assertEqual(result, [])
        mock_flash.assert_called_with(
            'An error occurred while processing your request. Check logs for more information.', 'error')
        mock_logger.error.assert_called()

    @patch('app.services.todo_service.flash')
    @patch('app.services.todo_service.logger')
    @patch('app.db.session.delete')
    def test_delete_todo(self, mock_delete, mock_logger, mock_flash):
        todo = ToDo(task='Test Task', description='Test Description')
        db.session.add(todo)
        db.session.commit()
        todo_service.delete_todo(todo.id)

        mock_delete.assert_called()
        mock_flash.assert_not_called()
        mock_logger.info.assert_called_with('Deleted to_do: <ToDo Test Task>')
        mock_logger.error.assert_not_called()

    @patch('app.services.todo_service.flash')
    @patch('app.services.todo_service.logger')
    @patch('app.db.session.delete')
    def test_delete_todo_fails_when_todo_not_found(self, mock_delete, mock_logger, mock_flash):
        todo = ToDo(task='Test Task', description='Test Description')
        db.session.add(todo)
        db.session.commit()
        todo_service.delete_todo(3)

        mock_delete.assert_not_called()
        mock_flash.assert_called_with(
            'Cannot delete a non-existing todo.', 'error')
        mock_logger.info.assert_not_called()
        mock_logger.error.assert_called_with('Todo item not found: ID 3')

    @patch('app.services.todo_service.flash')
    @patch('app.services.todo_service.logger')
    def test_edit_todo_description(self, mock_logger, mock_flash):
        todo = ToDo(task='Test Task', description='Test Description')
        db.session.add(todo)
        db.session.commit()
        todo_service.edit_todo(todo.id, task='Test Task',
                               description='New Description')
        updated_todo = ToDo.query.get(todo.id)
        print("\nupdated" + str(updated_todo))

        self.assertEqual(updated_todo.description, 'New Description')
        mock_flash.assert_not_called()
        mock_logger.info.assert_called_with('Updated to_do: <ToDo Test Task>')
        mock_logger.error.assert_not_called()

    @patch('app.services.todo_service.flash')
    @patch('app.services.todo_service.logger')
    def test_edit_todo_task(self, mock_logger, mock_flash):
        todo = ToDo(task='Test Task', description='Test Description')
        db.session.add(todo)
        db.session.commit()
        todo_service.edit_todo(todo.id, task='New Task',
                               description='Test Description')
        updated_todo = ToDo.query.get(todo.id)

        self.assertEqual(updated_todo.task, 'New Task')
        mock_flash.assert_not_called()
        mock_logger.info.assert_called_with('Updated to_do: <ToDo New Task>')
        mock_logger.error.assert_not_called()

    @patch('app.services.todo_service.flash')
    @patch('app.services.todo_service.logger')
    def test_edit_todo_fails_when_task_is_empty(self, mock_logger, mock_flash):
        todo = ToDo(task='Test Task', description='Test Description')
        db.session.add(todo)
        db.session.commit()
        todo_service.edit_todo(
            todo.id, task='', description='Test Description')
        updated_todo = ToDo.query.get(todo.id)

        self.assertEqual(updated_todo.task, 'Test Task')
        mock_flash.assert_called_with('Task cannot be empty.', 'error')
        mock_logger.info.assert_not_called()
        mock_logger.error.assert_called_with(
            'Error updating to_do: Task cannot be empty.')

    @patch('app.services.todo_service.flash')
    @patch('app.services.todo_service.logger')
    def test_edit_todo_fails_when_todo_not_found(self, mock_logger, mock_flash):
        todo = ToDo(task='Test Task', description='Test Description')
        db.session.add(todo)
        db.session.commit()
        todo_service.edit_todo(
            3, task='New Task', description='Test Description')
        updated_todo = ToDo.query.get(todo.id)

        self.assertEqual(updated_todo.task, 'Test Task')
        mock_flash.assert_called_with(
            'Cannot edit a non-existing todo.', 'error')
        mock_logger.info.assert_not_called()
        mock_logger.error.assert_called_with('Todo item not found: ID 3')

    @patch('app.services.todo_service.flash')
    @patch('app.services.todo_service.logger')
    def test_edit_todo_fails_when_task_exceeds_max_length(self, mock_logger, mock_flash):
        todo = ToDo(task='Test Task', description='Test Description')
        db.session.add(todo)
        db.session.commit()
        todo_service.edit_todo(todo.id, task='x' * 33,
                               description='Test Description')
        updated_todo = ToDo.query.get(todo.id)

        self.assertEqual(updated_todo.task, 'Test Task')
        mock_flash.assert_called_with(
            'Task exceeds maximum length of 32 characters', 'error')
        mock_logger.info.assert_not_called()
        mock_logger.error.assert_called_with(
            'Error updating to_do: Task exceeds maximum length of 32 characters')

    @patch('app.services.todo_service.flash')
    @patch('app.services.todo_service.logger')
    def test_edit_todo_fails_when_description_exceeds_max_length(self, mock_logger, mock_flash):
        todo = ToDo(task='Test Task', description='Test Description')
        db.session.add(todo)
        db.session.commit()
        todo_service.edit_todo(todo.id, task='Test Task',
                               description='x' * 300)
        updated_todo = ToDo.query.get(todo.id)

        self.assertEqual(updated_todo.description, 'Test Description')
        mock_flash.assert_called_with(
            'Description exceeds maximum length of 256 characters', 'error')
        mock_logger.info.assert_not_called()
        mock_logger.error.assert_called_with(
            'Error updating to_do: Description exceeds maximum length of 256 characters')


if __name__ == '__main__':
    unittest.main(verbosity=2)
