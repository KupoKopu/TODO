class TodoNotFoundException(Exception):
    """Exception raised when a todo item is not found in the database."""

    def __init__(self, todo_id, message="Todo item not found"):
        self.todo_id = todo_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: ID {self.todo_id}'
