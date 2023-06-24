from sqlalchemy import Table, Column, Integer, ForeignKey

from app.db.base import Base


association_table = Table(
    "user_task",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("task_id", Integer, ForeignKey("task.id"), primary_key=True),
)
