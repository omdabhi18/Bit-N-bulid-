import enum
import uuid
from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from Database.connection import Base


class FieldStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class Field(Base):

    __tablename__ = "fields"

    id = Column(String(50), primary_key=True, default=lambda: f"field-{uuid.uuid4().hex[:4]}") # e.g. "field-a"
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(120), nullable=False)
    area = Column(Float, default=5.0)
    crop_name = Column(String(100), default="Cotton")
    stage = Column(String(100), default="Flowering")

    health_score = Column(Integer, default=80)
    soil_moisture = Column(Float, default=35.0)
    status = Column(String(30), default="WARNING") # HEALTHY | WARNING | CRITICAL
    risk_category = Column(String(100), default="Water Stress")
    pest_risk = Column(String(50), default="Low (15%)")
    soil_ph = Column(Float, default=6.8)
    nitrogen = Column(String(50), default="Normal")
    phosphorus = Column(String(50), default="Optimal")
    potassium = Column(String(50), default="High")
    boundary = Column(JSON, default=list) # [{lat, lng}, ...]
    color = Column(String(20), default="#eab308")
    drip_status = Column(String(50), default="Ready")
    recommendation = Column(String(255), default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    farm = relationship("Farm", back_populates="fields")
    crops = relationship("Crop", back_populates="field", cascade="all, delete-orphan")
    sensors = relationship("Sensor", back_populates="field", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="field", cascade="all, delete-orphan")
    ai_advisories = relationship("AIAdvisory", back_populates="field", cascade="all, delete-orphan")
    action_plans = relationship("ActionPlan", back_populates="field", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="field", cascade="all, delete-orphan")
    disease_analyses = relationship("DiseaseAnalysis", back_populates="field", cascade="all, delete-orphan")
    expert_requests = relationship("ExpertRequest", back_populates="field", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="field", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="field")
