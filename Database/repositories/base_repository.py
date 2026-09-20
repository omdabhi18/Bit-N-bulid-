from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from Database.connection import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        result = await self.session.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        return list(result.scalars().all())

    async def create(self, entity: Optional[ModelType] = None, **kwargs) -> ModelType:
        if entity is None:
            entity = self.model(**kwargs)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, id: Any, **kwargs) -> Optional[ModelType]:
        entity = await self.get_by_id(id)
        if not entity:
            return None
        for k, v in kwargs.items():
            setattr(entity, k, v)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity


    async def delete_by_id(self, id: Any) -> bool:
        result = await self.session.execute(delete(self.model).filter(self.model.id == id))
        await self.session.commit()
        return result.rowcount > 0
