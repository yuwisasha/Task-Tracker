from typing import Any, Dict, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> ModelType | None:
        stmt = select(self.model).filter(self.model.id == id)
        return await db.execute(stmt)

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        return await db.execute(stmt)

    async def create(
        self, db: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        stmt = select(self.model).filter(id == id)
        obj = await db.execute(stmt)
        db.delete(obj)
        await db.commit()
        return obj
