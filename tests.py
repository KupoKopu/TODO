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


if __name__ == '__main__':
    unittest.main(verbosity=2)
