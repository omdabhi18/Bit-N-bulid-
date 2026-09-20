from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Database.models.sensor import Sensor
from Database.models.sensor_reading import SensorReading
from Database.repositories.base_repository import BaseRepository

class SensorRepository(BaseRepository[Sensor]):
    def __init__(self, session: AsyncSession):
        super().__init__(Sensor, session)

    async def get_by_device_id(self, device_id: str) -> Optional[Sensor]:
        res = await self.session.execute(select(Sensor).filter(Sensor.device_id == device_id))
        return res.scalars().first()

    async def get_sensors_for_farm(self, farm_id: str) -> List[Sensor]:
        res = await self.session.execute(select(Sensor).filter(Sensor.farm_id == farm_id))
        return list(res.scalars().all())

    async def add_reading(
        self,
        reading: Optional[SensorReading] = None,
        sensor_id: Optional[str] = None,
        value: Optional[float] = None,
        unit: str = "%",
        **kwargs
    ) -> SensorReading:
        if reading is None:
            reading = SensorReading(
                sensor_id=sensor_id,
                value=value,
                unit=unit,
                **kwargs
            )
        self.session.add(reading)
        await self.session.commit()
        await self.session.refresh(reading)
        return reading

    async def get_recent_readings(self, sensor_id: str, limit: int = 10) -> List[SensorReading]:
        res = await self.session.execute(
            select(SensorReading)
            .filter(SensorReading.sensor_id == sensor_id)
            .order_by(SensorReading.timestamp.desc())
            .limit(limit)
        )
        return list(res.scalars().all())


    async def get_latest_reading(self, sensor_id: str) -> Optional[SensorReading]:
        res = await self.session.execute(
            select(SensorReading)
            .filter(SensorReading.sensor_id == sensor_id)
            .order_by(SensorReading.timestamp.desc())
            .limit(1)
        )
        return res.scalars().first()

    async def get_paginated_readings(
        self,
        sensor_id: Optional[str] = None,
        field_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[SensorReading]:
        query = select(SensorReading)
        if sensor_id:
            query = query.filter(SensorReading.sensor_id == sensor_id)
        if field_id:
            query = query.filter(SensorReading.field_id == field_id)
        if start_time:
            query = query.filter(SensorReading.timestamp >= start_time)
        if end_time:
            query = query.filter(SensorReading.timestamp <= end_time)

        query = query.order_by(SensorReading.timestamp.desc()).offset(offset).limit(limit)
        res = await self.session.execute(query)
        return list(res.scalars().all())
