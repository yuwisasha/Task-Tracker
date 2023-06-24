from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.db.base import Base
from app.models.user_task import association_table


class Task(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(40))
    description: Mapped[str]
    deadline: Mapped[datetime]
    performer = relationship(
        "User",
        secondary=association_table,
        back_populates="tasks",
    )
