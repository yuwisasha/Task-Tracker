from __future__ import annotations

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


# Receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Receive via API on update
class UserUpdate(UserBase):
    password: str | None = None
    tasks: list[Task] | None = None


class UserInDBBase(UserBase):
    id: int | None = None

    class Config:
        orm_mode = True


# Return via API
class User(UserInDBBase):
    pass


# Store in db
class UserInDB(UserInDBBase):
    hashed_password: str


# Update references for Pydantic nested models
from .task import Task  # noqa

UserUpdate.update_forward_refs()
