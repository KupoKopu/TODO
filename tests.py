import os
import unittest

import sqlalchemy as sa

from app import app, db
from app.models import ToDo

os.environ['DATABASE_URL'] = 'sqlite://'


class ToDoModelCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
