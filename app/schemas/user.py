from __future__ import annotations

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: str | None = None
    # TODO tasks: list[Task] | None = None


class UserInDBBase(UserBase):
    id: int | None = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    # TODO tasks: list[Task] | None = None
    pass


class UserInDB(UserInDBBase):
    hashed_password: str

from .task import Task  # noqa
UserUpdate.update_forward_refs()
# TODO User.update_forward_refs()
