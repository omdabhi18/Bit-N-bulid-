from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Database.models.farm import Farm
from Database.models.field import Field
from Database.models.crop import Crop
from Database.repositories.base_repository import BaseRepository

class FarmRepository(BaseRepository[Farm]):
    def __init__(self, session: AsyncSession):
        super().__init__(Farm, session)

    async def get_by_owner_id(self, owner_id: str) -> List[Farm]:
        res = await self.session.execute(select(Farm).filter(Farm.owner_id == owner_id))
        return list(res.scalars().all())

    async def list_by_owner(self, owner_id: str) -> List[Farm]:
        return await self.get_by_owner_id(owner_id)

    async def get_with_fields(self, farm_id: str) -> Optional[Farm]:
        return await self.get_by_id(farm_id)


    async def get_fields_for_farm(self, farm_id: str) -> List[Field]:
        res = await self.session.execute(select(Field).filter(Field.farm_id == farm_id))
        return list(res.scalars().all())

    async def get_crops_for_farm(self, farm_id: str) -> List[Crop]:
        res = await self.session.execute(select(Crop).filter(Crop.farm_id == farm_id))
        return list(res.scalars().all())
