from sqlalchemy import Column, String, Integer, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class Risk(Base):
    __tablename__ = "risks"

    id = Column(String, primary_key=True, default=lambda: f"risk-{uuid.uuid4().hex[:4]}")
    farm_id = Column(String, ForeignKey("farms.id"), nullable=False)
    category = Column(String, nullable=False)
    icon = Column(String, default="AlertTriangle")
    severity = Column(String, default="High") # High | Critical | Medium | Low
    field = Column(String, default="Field A (Cotton)")
    probability = Column(Integer, default=80) # percentage
    indicators = Column(JSON, default=list) # list of evidence strings
    recommended_action = Column(String, nullable=False)
    plan_generated = Column(Boolean, default=False)
    plan_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    farm = relationship("Farm", back_populates="risks")
