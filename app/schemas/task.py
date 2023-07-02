from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class TaskBase(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None


# Receive via API on creation
class TaskCreate(TaskBase):
    title: str
    description: str
    performers: list[User] | None = None

    class Config:
        orm_mode = True


# Receive via API on update
class TaskUpdate(TaskBase):
    deadline: datetime = None
    performers: list[User] | None = None


class TaskInDBBase(TaskBase):
    id: int

    class Config:
        orm_mode = True


# Return via API
class Task(TaskInDBBase):
    pass


# Stored in db
class TaskInDB(TaskInDBBase):
    pass


# Update references for Pydantic nested models
from .user import User  # noqa

TaskCreate.update_forward_refs()
TaskUpdate.update_forward_refs()
