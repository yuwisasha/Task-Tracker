from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from app.core.config import settings


engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=False)
AsyncSessionLocal = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)
