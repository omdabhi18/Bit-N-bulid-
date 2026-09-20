import enum
from sqlalchemy import Column, String, Integer, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from Database.connection import Base

class AdvisoryStatus(str, enum.Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

class AIAdvisory(Base):

    __tablename__ = "ai_advisories"

    id = Column(String(50), primary_key=True, default=lambda: f"adv-{uuid.uuid4().hex[:4]}")
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="CASCADE"), nullable=True, index=True)
    field_id = Column(String(50), ForeignKey("fields.id", ondelete="CASCADE"), nullable=True, index=True)
    risk_id = Column(String(50), ForeignKey("risks.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(200), nullable=False)
    title_gu = Column(String(200), nullable=True)
    title_hi = Column(String(200), nullable=True)
    recommendation = Column(String(500), nullable=False)
    reasoning = Column(String(1000), default="")
    priority = Column(String(30), default="High")
    confidence = Column(Integer, default=90)
    status = Column(String(30), default="PENDING_APPROVAL", index=True) # PENDING_APPROVAL | APPROVED | REJECTED
    timestamp = Column(String(50), default="Today")
    orchestrator_summary = Column(String(500), default="Autonomous agricultural advisory")

    explainability = Column(JSON, default=dict)
    action_details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    farm = relationship("Farm", back_populates="ai_advisories")
    field = relationship("Field", back_populates="ai_advisories")
    risk = relationship("Risk", back_populates="advisories")
    action_plans = relationship("ActionPlan", back_populates="advisory", cascade="all, delete-orphan")
