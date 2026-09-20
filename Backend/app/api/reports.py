from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.notification_service import notification_service
from app.schemas.notification import AuditCertificateResponse

router = APIRouter(prefix="/reports", tags=["Farm Reports"])

@router.get("/audit-certificate", response_model=AuditCertificateResponse)
async def get_audit_certificate(db: AsyncSession = Depends(get_db)):
    return await notification_service.get_audit_certificate(db)
