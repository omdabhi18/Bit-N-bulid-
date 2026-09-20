from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any

class ActivityLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    time: str
    agent: str
    event: str
    severity: str # info | success | warning | error

class AlertNotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    severity: str
    isRead: str
    channel: str
    createdAt: str

class AuditCertificateResponse(BaseModel):
    farmName: str
    farmerName: str
    healthScore: int
    village: str
    district: str
    generatedAt: str
    verifiedAgentsCount: int
    totalDecisionsLogged: int
    recentAuditLogs: List[ActivityLogResponse]
