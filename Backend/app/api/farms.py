from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.farm_service import farm_service
from app.schemas.farm import FarmProfile, FieldDetail

router = APIRouter(prefix="/farms", tags=["Farms & Fields"])

@router.get("/profile", response_model=FarmProfile)
async def get_profile(db: AsyncSession = Depends(get_db)):
    profile = await farm_service.get_farm_profile(db)
    if not profile:
        raise HTTPException(status_code=404, detail="Farm profile not found")
    return profile

@router.get("/fields", response_model=List[FieldDetail])
async def get_all_fields(db: AsyncSession = Depends(get_db)):
    return await farm_service.get_fields(db)

@router.get("/{farm_id}/fields", response_model=List[FieldDetail])
async def get_farm_fields(farm_id: str, db: AsyncSession = Depends(get_db)):
    return await farm_service.get_fields(db, farm_id)
