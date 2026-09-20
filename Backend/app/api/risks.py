from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.risk_service import risk_service
from app.schemas.risk import RiskResponse

router = APIRouter(prefix="/risks", tags=["Risk Detection"])

@router.get("", response_model=List[RiskResponse])
async def get_risks(db: AsyncSession = Depends(get_db)):
    return await risk_service.get_risks(db)

@router.post("/{risk_id}/generate-plan")
async def generate_plan_from_risk(risk_id: str, db: AsyncSession = Depends(get_db)):
    plan_id = await risk_service.generate_plan_from_risk(db, "farm-greenvalley-01", risk_id)
    if not plan_id:
        raise HTTPException(status_code=404, detail="Risk not found")
    return {"success": True, "planId": plan_id, "message": f"Action Plan {plan_id} created by Constrained Planner"}
