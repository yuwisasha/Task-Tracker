from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None


class TaskCreate(TaskBase):
    title: str
    description: str


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
