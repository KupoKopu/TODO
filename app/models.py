import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, validates

from app import db


class ToDo(db.Model):
    """ToDo model for storing tasks and their descriptions."""

    __tablename__ = 'to_do'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(
        sa.VARCHAR(32), index=True, nullable=False)
    description: Mapped[str] = mapped_column(sa.VARCHAR(256), nullable=True)

    @validates('description')
    def validate_description(self, key, description):
        max_length = 256
        if description and len(description) > max_length:
            raise ValueError(f"Description exceeds maximum length of {max_length} characters")  # noqa
        return description

    @validates('task')
    def validate_task(self, key, task):
        max_length = 32
        if task and len(task) > max_length:
            raise ValueError(f"Task exceeds maximum length of {max_length} characters")  # noqa
        return task

    def __repr__(self):
        return f'<ToDo {self.task}>'
