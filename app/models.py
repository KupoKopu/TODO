import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class ToDo(db.Model):
    """ToDo model for storing tasks and their descriptions."""

    __tablename__ = 'to_do'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(
        sa.String(32), index=True, nullable=False)
    description: Mapped[str] = mapped_column(sa.String(256), index=True)

    def __repr__(self):
        return f'<ToDo {self.task}>'
