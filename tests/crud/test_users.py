import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.core.security import verify_password
from tests.utils.utils import random_lower_string, random_email, random_name


@pytest.mark.asyncio
async def test_create_user(db: AsyncSession) -> None:
    email = random_email()
    name = random_name()
    password = random_lower_string()
    user_in = schemas.UserCreate(
        email=email,
        name=name,
        password=password,
    )
    user = await crud.user.create(db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


@pytest.mark.asyncio
async def test_auth_user(db: AsyncSession) -> None:
    email = random_email()
    name = random_name()
    password = random_lower_string()
    user_in = schemas.UserCreate(
        email=email,
        name=name,
        password=password,
    )
    user = await crud.user.create(db, obj_in=user_in)
    auth_user = await crud.user.authenticate(
        db, email=email, password=password
    )
    assert auth_user
    assert user.email == auth_user.email


@pytest.mark.asyncio
async def test_not_auth_user(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user = await crud.user.authenticate(db, email=email, password=password)
    assert user is None


@pytest.mark.asyncio
async def test_get_user(db: AsyncSession) -> None:
    email = random_email()
    name = random_name()
    password = random_lower_string()
    user_in = schemas.UserCreate(
        email=email,
        name=name,
        password=password,
    )
    user = await crud.user.create(db, obj_in=user_in)
    user_2 = await crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email


@pytest.mark.asyncio
async def test_update_user(db: AsyncSession) -> None:
    email = random_email()
    name = random_name()
    password = random_lower_string()
    user_in = schemas.UserCreate(
        email=email,
        name=name,
        password=password,
    )
    user = await crud.user.create(db, obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = schemas.UserUpdate(
        password=new_password,
    )
    await crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = await crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert await verify_password(new_password, user_2.hashed_password)
