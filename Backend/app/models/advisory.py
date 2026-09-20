from sqlalchemy import Column, String, Integer, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class AIAdvisory(Base):
    __tablename__ = "ai_advisories"

    id = Column(String, primary_key=True, default=lambda: f"adv-{uuid.uuid4().hex[:4]}")
    farm_id = Column(String, ForeignKey("farms.id"), nullable=False)
    title = Column(String, nullable=False)
    title_gu = Column(String, nullable=True)
    title_hi = Column(String, nullable=True)
    field = Column(String, default="Field A (Cotton)")
    priority = Column(String, default="High")
    confidence_score = Column(Integer, default=90)
    status = Column(String, default="Pending Approval") # Pending Approval | Approved | Rejected
    timestamp = Column(String, default="Today")
    orchestrator_summary = Column(String, nullable=False)
    explainability = Column(JSON, default=dict) # { factors: [...], whyText: "..." }
    action_details = Column(JSON, default=dict) # { action, volume, duration, zone, costEstimate, waterSource }
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    farm = relationship("Farm", back_populates="advisories")
