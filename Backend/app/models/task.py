from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import random
from app.database import Base

class FarmTask(Base):
    __tablename__ = "farm_tasks"

    id = Column(String, primary_key=True, default=lambda: f"TSK-{random.randint(10, 99)}")
    farm_id = Column(String, ForeignKey("farms.id"), nullable=False)
    plan_id = Column(String, ForeignKey("action_plans.id"), nullable=True)
    title = Column(String, nullable=False)
    field = Column(String, default="Field A")
    status = Column(String, default="todo") # todo | in-progress | completed
    priority = Column(String, default="High")
    due_time = Column(String, default="Today 18:00")
    assigned_to = Column(String, default="Kishanbhai Patel")
    icon = Column(String, default="CheckCircle")
    notes = Column(String, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    farm = relationship("Farm", back_populates="tasks")
    action_plan = relationship("ActionPlan", back_populates="tasks")
