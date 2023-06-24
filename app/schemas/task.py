from datetime import datetime

from pydantic import BaseModel

from app.models.user import User


class TaskBase(BaseModel):
    title: str | None = None
    description: str | None = None


class TaskCreate(TaskBase):
    title: str
    description: str


class TaskUpdate(TaskBase):
    pass


class TaskInDBBase(TaskBase):
    id: int
    title: str
    performers: list[User]

    class Config:
        orm_mode = True


class Task(TaskInDBBase):
    deadline: datetime


class TaskInDB(TaskInDBBase):
    pass
