from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.db.base import Base
from app.models.user_task import association_table

if TYPE_CHECKING:
    from .task import Task  # noqa


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String(40), unique=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(40))
    tasks = relationship(
        "Task",
        secondary=association_table,
        back_populates="performers",
    )
    hashed_password: Mapped[str] = mapped_column(nullable=False)
