from sqlalchemy import Column, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from Database.connection import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(String(50), primary_key=True, default=lambda: f"LOG-{uuid.uuid4().hex[:4].upper()}")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="CASCADE"), nullable=True, index=True)
    field_id = Column(String(50), ForeignKey("fields.id", ondelete="SET NULL"), nullable=True, index=True)
    agent = Column(String(100), default="Master Orchestrator")
    event = Column(String(500), nullable=True, default="")
    event_type = Column(String(100), default="ORCHESTRATION_DECISION")

    description = Column(String(500), default="")
    entity_type = Column(String(50), nullable=True) # e.g. "ActionPlan", "Task", "Sensor"
    entity_id = Column(String(50), nullable=True)
    time = Column(String(50), default="Just now")
    severity = Column(String(20), default="info") # info | success | warning | error
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relationships
    user = relationship("User", back_populates="activity_logs")
    farm = relationship("Farm", back_populates="activity_logs")
    field = relationship("Field", back_populates="activity_logs")
