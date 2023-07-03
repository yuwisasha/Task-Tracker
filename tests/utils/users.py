from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from .utils import random_lower_string, random_email
from app.models.user import User
from app import crud, schemas
from app.core.config import settings


# Get a token for test endpoints which need auth user
async def get_auth_token_header(
    client: AsyncClient, email: str, password: str
) -> dict[str, str]:
    login_data = {
        "username": email,
        "password": password,
    }
    response = await client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data
    )
    token = response.json()
    access_token = token["access_token"]
    header = {"Authorization": f"Bearer {access_token}"}
    return header


async def create_random_user(db: AsyncSession, password: str = None) -> User:
    name = random_lower_string()
    email = random_email()
    if password is None:
        password = random_lower_string()
    user_in = schemas.UserCreate(
        name=name,
        email=email,
        password=password,
    )
    user = await crud.user.create(db, obj_in=user_in)
    return user
