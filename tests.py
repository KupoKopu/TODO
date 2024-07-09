import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
import sqlalchemy as sa
from app import app, db
from app.models import ToDo

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

        todos = db.session.scalars(sa.select(ToDo)).all()

        self.assertEqual(todos, [], "no todos at start")

        todo = ToDo(task="test", description="test description")

        db.session.add(todo)
        db.session.commit()

        todos = db.session.scalars(sa.select(ToDo)).all()

        self.assertEqual(todos.__len__(), 1, "todo has inserted")

if __name__ == '__main__':
    unittest.main(verbosity=2)
