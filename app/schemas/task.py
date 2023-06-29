from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None


class TaskCreate(TaskBase):
    title: str
    description: str
    performers: list[User] | None = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Task title",
                "description": "Task description",
                "deadline": "2023-06-25 15:31:44",
                "performers": [
                    {
                        "id": 1,
                        "email": "user@example.com",
                        "name": "string",
                    }
                ],
            }
        }


class TaskUpdate(TaskBase):
    deadline: datetime


class TaskInDBBase(TaskBase):
    id: int

    class Config:
        orm_mode = True


class Task(TaskInDBBase):
    pass


class TaskInDB(TaskInDBBase):
    pass


from .user import User  # noqa

TaskCreate.update_forward_refs()
