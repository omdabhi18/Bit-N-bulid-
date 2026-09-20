from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.advisory_service import advisory_service
from app.schemas.advisory import AdvisoryResponse, AdvisoryActionRequest

router = APIRouter(prefix="/advisory", tags=["AI Advisory"])

@router.get("", response_model=List[AdvisoryResponse])
async def get_advisories(db: AsyncSession = Depends(get_db)):
    return await advisory_service.get_advisories(db)

@router.post("/{advisory_id}/approve")
async def approve_advisory(advisory_id: str, db: AsyncSession = Depends(get_db)):
    success = await advisory_service.approve_advisory(db, advisory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Advisory not found")
    return {"success": True, "message": "Advisory approved and dispatched to execution pipeline"}

@router.post("/{advisory_id}/reject")
async def reject_advisory(advisory_id: str, req: AdvisoryActionRequest = None, db: AsyncSession = Depends(get_db)):
    reason = req.reason if req else "Farmer decided to delay"
    success = await advisory_service.reject_advisory(db, advisory_id, reason)
    if not success:
        raise HTTPException(status_code=404, detail="Advisory not found")
    return {"success": True, "message": "Advisory dismissed and logged"}
