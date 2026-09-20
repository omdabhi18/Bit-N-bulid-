from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.dashboard_service import dashboard_service
from app.schemas.dashboard import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardResponse)
async def get_dashboard_data(db: AsyncSession = Depends(get_db)):
    return await dashboard_service.get_dashboard(db)
