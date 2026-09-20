from sqlalchemy import Column, String, Integer, Float, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import random
from app.database import Base

class ActionPlan(Base):
    __tablename__ = "action_plans"

    id = Column(String, primary_key=True, default=lambda: f"PLAN-{random.randint(1000, 9999)}")
    farm_id = Column(String, ForeignKey("farms.id"), nullable=False)
    title = Column(String, nullable=False)
    target_field = Column(String, default="Field A (Cotton - 5.2 Acres)")
    action_type = Column(String, nullable=False)
    scheduled_time = Column(String, default="Today • 18:00 IST")
    status = Column(String, default="Draft") # Draft | Approved | Scheduled | In Progress | Completed | Cancelled
    priority = Column(String, default="High")
    estimated_cost = Column(Float, default=45.0)
    water_volume = Column(String, default="2,500 L")
    constraints = Column(JSON, default=dict) # { costBudget, weatherWindow, waterAvailability, safetyProtocols }
    hardware_target = Column(String, default="Solenoid Valve SV-01 (Field A)")
    assigned_to = Column(String, default="Kishanbhai Patel")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    farm = relationship("Farm", back_populates="action_plans")
    tasks = relationship("FarmTask", back_populates="action_plan", cascade="all, delete-orphan")
