import unittest
from unittest.mock import patch

from app.exceptions.exceptions import TodoNotFoundException
from app.models import ToDo
from app.services.todo_service import edit_todo, get_todo_by_id


class EditTodoTestCase(unittest.TestCase):
    @patch('app.services.todo_service.db')
    def test_edit_todo_success(self, mock_db):
        # Arrange
        todo_id = 1
        task = 'New Task'
        description = 'New Description'
        todo = ToDo.query.get.return_value
        mock_session = mock_db.session.return_value

        # Act
        edit_todo(todo_id, task, description)

        # Assert
        self.assertEqual(todo.task, task)
        self.assertEqual(todo.description, description)
        mock_session.commit.assert_called_once()

    @patch('app.services.todo_service.db')
    def test_edit_todo_todo_not_found(self, mock_db):
        # Arrange
        todo_id = 1
        task = 'New Task'
        description = 'New Description'
        ToDo.query.get.return_value = None
        mock_session = mock_db.session.return_value

        # Act
        edit_todo(todo_id, task, description)

        # Assert
        mock_session.rollback.assert_called_once()
        self.assertEqual(mock_db.session.delete.call_count, 0)
        self.assertEqual(mock_db.session.commit.call_count, 0)

    @patch('app.services.todo_service.db')
    def test_edit_todo_empty_task(self, mock_db):
        # Arrange
        todo_id = 1
        task = ''
        description = 'New Description'
        todo = ToDo.query.get.return_value
        mock_session = mock_db.session.return_value

        # Act
        edit_todo(todo_id, task, description)

        # Assert
        mock_session.rollback.assert_called_once()
        self.assertEqual(mock_db.session.commit.call_count, 0)
        self.assertEqual(mock_db.session.delete.call_count, 0)

    @patch('app.services.todo_service.db')
    def test_edit_todo_exception(self, mock_db):
        # Arrange
        todo_id = 1
        task = 'New Task'
        description = 'New Description'
        ToDo.query.get.side_effect = TodoNotFoundException(todo_id)
        mock_session = mock_db.session.return_value

        # Act
        edit_todo(todo_id, task, description)

        # Assert
        mock_session.rollback.assert_called_once()
        self.assertEqual(mock_db.session.commit.call_count, 0)
        self.assertEqual(mock_db.session.delete.call_count, 0)
        self.assertEqual(mock_db.session.rollback.call_count, 1)


if __name__ == '__main__':
    unittest.main()


class GetTodoByIdTestCase(unittest.TestCase):
    @patch('app.services.todo_service.db')
    def test_get_todo_by_id_success(self, mock_db):
        # Arrange
        todo_id = 1
        todo = ToDo.query.get.return_value

        # Act
        result = get_todo_by_id(todo_id)

        # Assert
        self.assertEqual(result, todo)

    @patch('app.services.todo_service.db')
    def test_get_todo_by_id_todo_not_found(self, mock_db):
        # Arrange
        todo_id = 1
        ToDo.query.get.return_value = None

        # Act
        result = get_todo_by_id(todo_id)

        # Assert
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
