from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.db.base import Base
from app.models.user_task import association_table

# Avoid circular import
if TYPE_CHECKING:
    from .user import User  # noqa


class Task(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(40))
    description: Mapped[str]
    deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    performers = relationship(
        "User",
        secondary=association_table,
        back_populates="tasks",
        lazy="selectin",
    )
