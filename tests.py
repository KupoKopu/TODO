import unittest

import sqlalchemy as sa
from flask import url_for

from app import create_app, db
from app.models import ToDo
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SERVER_NAME = 'localhost.localdomain'
    WTF_CSRF_ENABLED = False


class ToDoModelCase(unittest.TestCase):
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

    def test_index_route(self):
        response = self.app.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'To Do', response.data)

    def test_add_route_get(self):
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
