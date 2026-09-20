from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_db
from app.services.disease_service import disease_service
from app.integrations.storage_provider import storage_service
from app.schemas.disease import (
    DiseaseCatalogItem,
    DiseaseAnalyzeResponse,
    EscalationCreateRequest,
    EscalationResponse
)

router = APIRouter(prefix="/disease", tags=["Crop Disease AI"])

@router.get("/catalog", response_model=List[DiseaseCatalogItem])
async def get_catalog():
    return disease_service.get_catalog()

@router.post("/analyze", response_model=DiseaseAnalyzeResponse)
async def analyze_crop_image(
    file: Optional[UploadFile] = File(None),
    sampleId: Optional[str] = Form(None),
    cropId: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    storage_info = None
    if file:
        file_bytes = await file.read()
        storage_info = await storage_service.upload_file(
            file_bytes=file_bytes,
            filename=file.filename or "crop.jpg",
            content_type=file.content_type or "image/jpeg",
            folder="crops"
        )
    return await disease_service.analyze_sample(
        sample_id=sampleId,
        crop_id=cropId,
        image_url=storage_info.get("url") if storage_info else None,
        storage_info=storage_info,
        db=db
    )

@router.get("/escalations", response_model=List[EscalationResponse])
async def get_escalations(db: AsyncSession = Depends(get_db)):
    return await disease_service.get_escalations(db)

@router.post("/escalate", response_model=EscalationResponse)
async def create_escalation(data: EscalationCreateRequest, db: AsyncSession = Depends(get_db)):
    return await disease_service.create_escalation(db, data)
