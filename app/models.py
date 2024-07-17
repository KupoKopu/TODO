import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, validates

from app import db


class ToDo(db.Model):
    """
    Represents a to-do item.

    Attributes:
        id (int): The unique identifier of the to-do item.
        task (str): The task description of the to-do item.
        description (str): The optional description of the to-do item.

    Methods:
        validate_description: Validates the length of the description attribute.
        validate_task: Validates the length of the task attribute.
        __repr__: Returns a string representation of the to-do item.
    """

    __tablename__ = 'to_do'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(
        sa.VARCHAR(32), index=True, nullable=False)
    description: Mapped[str] = mapped_column(sa.VARCHAR(256), nullable=True)

    @validates('description')
    def validate_description(self, key, description):
        """
        Validates the length of the description attribute.

        Args:
            key (str): The name of the attribute being validated.
            description (str): The value of the description attribute.

        Raises:
            ValueError: If the description exceeds the maximum length.

        Returns:
            str: The validated description.
        """
        max_length = 256
        if description and len(description) > max_length:
            raise ValueError(f"Description exceeds maximum length of {max_length} characters")  # noqa
        return description

    @validates('task')
    def validate_task(self, key, task):
        """
        Validates the length of the task attribute.

        Args:
            key (str): The name of the attribute being validated.
            task (str): The value of the task attribute.

        Raises:
            ValueError: If the task exceeds the maximum length.

        Returns:
            str: The validated task.
        """
        max_length = 32
        if task and len(task) > max_length:
            raise ValueError(f"Task exceeds maximum length of {max_length} characters")  # noqa
        return task

    def __repr__(self):
        """
        Returns a string representation of the to-do item.

        Returns:
            str: The string representation of the to-do item.
        """
        return f'<ToDo {self.task}>'
