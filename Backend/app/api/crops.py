from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import Optional
from app.database import get_db
from app.models.crop import Crop
from app.schemas.farm import CropItem, CropCatalogResponse

router = APIRouter(prefix="/crops", tags=["Crops"])

@router.get("", response_model=CropCatalogResponse)
async def get_crops(
    search: Optional[str] = Query(None, description="Search term matching English or Gujarati crop name"),
    category: Optional[str] = Query(None, description="Filter by crop category"),
    disease_ai_supported: Optional[bool] = Query(None, description="Filter by AI disease vision capability"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Crop).where(Crop.is_active.is_(True))

    if search:
        term = f"%{search.strip()}%"
        query = query.where(
            or_(
                Crop.name.ilike(term),
                Crop.name_gujarati.ilike(term)
            )
        )

    if category:
        query = query.where(Crop.category.ilike(f"%{category.strip()}%"))

    if disease_ai_supported is not None:
        query = query.where(Crop.disease_ai_supported.is_(disease_ai_supported))

    query = query.order_by(Crop.name.asc())
    res = await db.execute(query)
    crops = res.scalars().all()

    items = [
        CropItem(
            id=c.id,
            name=c.name,
            name_gujarati=c.name_gujarati,
            category=c.category or "Cash Crop",
            scientific_name=c.scientific_name,
            disease_ai_supported=bool(c.disease_ai_supported),
            is_active=bool(c.is_active),
            variety=c.variety or "Standard Variety",
            stage=c.stage or "Vegetative",
            area=c.area or 5.0,
            field=c.field_name or "Field A",
            sowingDate=c.sowing_date or "2026-06-15"
        )
        for c in crops
    ]

    return CropCatalogResponse(success=True, crops=items)

