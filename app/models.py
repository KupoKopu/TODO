from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class ToDo(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    task: so.Mapped[str] = so.mapped_column(sa.String(32), index=True,
                                                unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(256), index=True,
                                             unique=True)
    def __repr__(self):
        return '<ToDo {}>'.format(self.task)