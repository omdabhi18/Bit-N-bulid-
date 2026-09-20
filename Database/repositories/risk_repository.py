from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Database.models.risk import Risk
from Database.repositories.base_repository import BaseRepository

class RiskRepository(BaseRepository[Risk]):
    def __init__(self, session: AsyncSession):
        super().__init__(Risk, session)

    async def get_active_risks_for_farm(self, farm_id: str) -> List[Risk]:
        res = await self.session.execute(
            select(Risk)
            .filter(Risk.farm_id == farm_id, Risk.status == "ACTIVE")
            .order_by(Risk.detected_at.desc())
        )
        return list(res.scalars().all())

    async def get_by_field_id(self, field_id: str) -> List[Risk]:
        res = await self.session.execute(
            select(Risk)
            .filter(Risk.field_id == field_id)
            .order_by(Risk.detected_at.desc())
        )
        return list(res.scalars().all())
