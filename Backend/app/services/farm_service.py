from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.models.farm import Farm, Field
from app.models.crop import Crop
from app.schemas.farm import FarmProfile, FieldDetail, Coordinate, CropItem

class FarmService:
    async def get_farm_profile(self, db: AsyncSession, farm_id: str = "farm-greenvalley-01") -> Optional[FarmProfile]:
        res = await db.execute(select(Farm).filter(Farm.id == farm_id))
        farm = res.scalars().first()
        if not farm:
            return None

        crop_res = await db.execute(select(Crop).filter(Crop.farm_id == farm_id))
        crops = crop_res.scalars().all()

        return FarmProfile(
            farmerName=farm.farmer_name,
            farmName=farm.name,
            village=farm.village,
            taluka=farm.taluka,
            district=farm.district,
            state=farm.state,
            totalAreaAcre=farm.total_area_acre,
            soilType=farm.soil_type,
            irrigationMethod=farm.irrigation_method,
            coordinates=Coordinate(lat=farm.latitude, lng=farm.longitude),
            crops=[CropItem(
                id=c.id,
                name=c.name,
                variety=c.variety,
                stage=c.stage,
                area=c.area,
                field=c.field_name,
                sowingDate=c.sowing_date
            ) for c in crops]
        )

    async def get_fields(self, db: AsyncSession, farm_id: str = "farm-greenvalley-01") -> List[FieldDetail]:
        res = await db.execute(select(Field).filter(Field.farm_id == farm_id))
        fields = res.scalars().all()
        return [
            FieldDetail(
                id=f.id,
                name=f.name,
                crop=f.crop,
                area=f.area,
                stage=f.stage,
                healthScore=f.health_score,
                soilMoisture=f.soil_moisture,
                status=f.status,
                riskCategory=f.risk_category,
                pestRisk=f.pest_risk,
                soilPH=f.soil_ph,
                nitrogen=f.nitrogen,
                phosphorus=f.phosphorus,
                potassium=f.potassium,
                sensorNode=f.sensor_node,
                sensorStatus=f.sensor_status,
                coordinates=[Coordinate(**c) for c in (f.coordinates or [])],
                color=f.color,
                dripStatus=f.drip_status,
                recommendation=f.recommendation
            ) for f in fields
        ]

farm_service = FarmService()
