from dataclasses import dataclass
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import verify_password


# Test dataclass representing data of user
@dataclass
class TestUser:
    __test__ = False

    EMAIL: str = "user@example.com"
    NAME: str = "user"
    PASSWORD: str = "user"
    NEW_EMAIL: str = "test@example.com"
    NEW_NAME: str = "example"
    NEW_PASSWORD: str = "example"


@pytest.mark.asyncio
async def test_create_user(db: AsyncSession) -> None:
    user_in = UserCreate(
        email=TestUser.EMAIL, name=TestUser.NAME, password=TestUser.PASSWORD
    )
    user = await crud.user.create(db, obj_in=user_in)
    assert user.email == TestUser.EMAIL
    assert hasattr(user, "hashed_password")


@pytest.mark.asyncio
async def test_auth_user(db: AsyncSession) -> None:
    auth_user = await crud.user.authenticate(
        db, email=TestUser.EMAIL, password=TestUser.PASSWORD
    )
    assert auth_user
    assert auth_user.email == TestUser.EMAIL


@pytest.mark.asyncio
async def test_get_user(db: AsyncSession) -> None:
    user = await crud.user.get_by_email(db, email=TestUser.EMAIL)
    assert user
    assert user.email == TestUser.EMAIL
    assert user.name == TestUser.NAME


@pytest.mark.asyncio
async def test_update_user(db: AsyncSession) -> None:
    new_password = TestUser.NEW_PASSWORD
    user = await crud.user.get_by_email(db, email=TestUser.EMAIL)
    user_in_update = UserUpdate(password=new_password)
    await crud.user.update(db, db_obj=user, obj_in=user_in_update)
    updated_user = await crud.user.get_by_email(db, email=TestUser.EMAIL)
    assert updated_user
    assert updated_user.email == user.email
    assert await verify_password(new_password, updated_user.hashed_password)


@pytest.mark.asyncio
async def test_delete_user(db: AsyncSession) -> None:
    user = await crud.user.get_by_email(db, email=TestUser.EMAIL)
    await crud.user.remove(db, id=user.id)
    deleted_user = await crud.user.get_by_email(db, email=TestUser.EMAIL)
    assert deleted_user is None
