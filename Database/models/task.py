import enum
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import random
from Database.connection import Base

class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

class TaskPriority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"

class Task(Base):

    __tablename__ = "tasks"

    id = Column(String(50), primary_key=True, default=lambda: f"TSK-{random.randint(10, 99)}")
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="CASCADE"), nullable=True, index=True)
    field_id = Column(String(50), ForeignKey("fields.id", ondelete="CASCADE"), nullable=True, index=True)

    action_plan_id = Column(String(50), ForeignKey("action_plans.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), default="")
    assigned_to = Column(String(120), default="Kishanbhai Patel")
    priority = Column(String(30), default="High")
    status = Column(String(30), default="TODO", index=True) # TODO, IN_PROGRESS, COMPLETED, CANCELLED
    due_at = Column(String(50), default="Today 18:00")
    due_time = Column(String(50), default="Today 18:00")
    icon = Column(String(50), default="CheckCircle")
    notes = Column(String(500), default="")
    failure_reason = Column(String(255), nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    farm = relationship("Farm", back_populates="tasks")
    field = relationship("Field", back_populates="tasks")
    action_plan = relationship("ActionPlan", back_populates="tasks")
