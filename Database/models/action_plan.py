import enum
from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import random
from Database.connection import Base

class ActionPlanStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class ActionPriority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class ActionPlan(Base):

    __tablename__ = "action_plans"

    id = Column(String(50), primary_key=True, default=lambda: f"PLAN-{random.randint(1000, 9999)}")
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="CASCADE"), nullable=True, index=True)
    field_id = Column(String(50), ForeignKey("fields.id", ondelete="CASCADE"), nullable=True, index=True)
    risk_id = Column(String(50), ForeignKey("risks.id", ondelete="SET NULL"), nullable=True, index=True)
    advisory_id = Column(String(50), ForeignKey("ai_advisories.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(200), default="Autonomous Farm Action Plan")
    target_field = Column(String(150), default="Field A (Cotton - 5.2 Acres)")
    action = Column(String(200), nullable=False)
    action_type = Column(String(150), default="Irrigation / Fertigation")

    scheduled_time = Column(String(100), default="Today • 18:00 IST")
    duration = Column(String(50), default="35 Minutes")
    estimated_cost = Column(Float, default=45.0)
    water_volume = Column(String(50), default="2,500 L")
    required_resources = Column(JSON, default=dict)
    weather_window = Column(String(150), default="Safe (Rain prob 12%, Wind 14 km/h)")

    safety_constraints = Column(String(200), default="Electrical line grounding verified")
    constraints = Column(JSON, default=dict)
    hardware_target = Column(String(120), default="Solenoid Valve SV-01 (Field A)")
    assigned_to = Column(String(120), default="Kishanbhai Patel")
    priority = Column(String(30), default="High")
    confidence = Column(Integer, default=92)
    status = Column(String(30), default="DRAFT", index=True) # DRAFT, PENDING_APPROVAL, APPROVED, SCHEDULED, EXECUTING, COMPLETED, FAILED, CANCELLED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    farm = relationship("Farm", back_populates="action_plans")
    field = relationship("Field", back_populates="action_plans")
    risk = relationship("Risk", back_populates="action_plans")
    advisory = relationship("AIAdvisory", back_populates="action_plans")
    tasks = relationship("Task", back_populates="action_plan", cascade="all, delete-orphan")
