from pydantic import BaseModel, EmailStr

from app.models.task import Task


class UserBase(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: int | None = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    tasks: list[Task]


class UserInDB(UserInDBBase):
    hashed_password: str
